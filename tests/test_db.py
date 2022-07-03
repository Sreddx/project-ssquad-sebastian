# tests.py
import unittest
from peewee import *
from app import TimelinePost, get_timeline_posts


MODELS=[TimelinePost]
#use an in-memory SQLite for tests.
test_db=SqliteDatabase(':memory:')

#print(test_db)
class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        #Bind model classes to test db.Since we have a complete list of
        #all models,we do not need to recursively bind dependencies.
        test_db.bind(MODELS,bind_refs=False,bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        #Not strictly necessary since SQLite in-memory databases only live
        #for the duration of the connection,and in the next step we close
        #the connection ... but a good practice all the same.
        test_db.drop_tables(MODELS)
        #Close connection to db.
        test_db.close()
    

    def test_timeline_post(self):
    #Create two timeline posts and verify if they exist
        first_post=TimelinePost.create(name='John Doe',email='john@example.com',content='Hello world,I\'mJohn!')
        assert first_post.id == 1
        second_post=TimelinePost.create(name='Jane Doe',email='jame@example.com',content='Hello world,I\'mJane!')
        assert second_post.id == 2
        #TODO:Get timeline posts and assert that they are correct

        #Check if length of list within dictionary is 2 as 2 posts were created previously. (Get funcion returns dictionary with list of posts)
        response = get_timeline_posts() #We call get posts function
        assert len(response["timeline_posts"]) == 2

        #Check if posts in list are the same as the ones inserted 2 is the first in the list and 1 is the second
        assert response["timeline_posts"][0]["name"] =='Jane Doe' #Jane Doe
        assert response["timeline_posts"][1]["name"] =='John Doe' #John Doe