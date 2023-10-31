from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )
    

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        if isinstance(name,str) and len(name):
            self._name = name
        else:
            raise ValueError
        
    @property
    def job_title(self):
        return self._job_title
    
    @job_title.setter
    def job_title(self,job_title):
        if isinstance(job_title,str) and len(job_title):
            self._job_title = job_title
        else:
            raise ValueError
        
        
    @property
    def employee_id(self):
        return self._employee_id
    
    @employee_id.setter
    def employee_id(self,employee_id):
        if isinstance(employee_id,int) and Employee.find_by_id(employee_id):
            self._employee_id = employee_id
        else:
            raise ValueError
        
    @property
    def summary(self):
        return self._summary
    
    @summary.setter
    def summary(self,summary):
        if isinstance(summary,str) and len(summary):
            self._summary = summary
        else:
            raise ValueError
        
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self,year):
        if isinstance(year,int) and year >= 2000:
            self._year = year
        else:
            raise ValueError

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""

        CURSOR.execute("INSERT INTO reviews (year,summary,employee_id) VALUES (?,?,?)", (self.year, self.summary, self.employee_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
       
        # Check the dictionary for  existing instance using the row's primary key
        review = cls.all.get(row[0])
        if review:
            # ensure attributes match row values in case local instance was modified
            review.year = row[1]
            review.summary = row[2]
            review.employee_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        review = CURSOR.execute("SELECT * FROM reviews WHERE id = ?",(id,)).fetchone()
        return cls.instance_from_db(review) if review else None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        CURSOR.execute('UPDATE reviews SET year = ?,summary=?,employee_id=? WHERE id = ?',(self.year,self.summary,self.employee_id,self.id))


    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        CURSOR.execute('DELETE FROM reviews WHERE id = ?',(self.id,))
         # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        rows = CURSOR.execute('SELECT * FROM reviews').fetchall()

        return [cls.instance_from_db(row) for row in rows]

