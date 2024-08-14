import os
os.chdir("../../../")

from etiket.db.get_db_session import get_db_session

from etiket.db.data_models.dataset import  DatasetCreate, DatasetRead,\
    DatasetUpdate, DatasetSearch, DatasetSelection
from etiket.db.data_models.scope import ScopeUpdate, ScopeCreate, ScopeRead

from etiket.db.data_access_objects.scope import dao_scope
from etiket.db.data_access_objects.dataset import dao_dataset

from uuid import uuid4
import unittest

from datetime import datetime

class test_dataset_stuff(unittest.TestCase):
    def test_create_and_read_update_delete_dataset(self):
        with get_db_session() as session:
            scope = _create_scope("test", session)
            
            datasetCreate1 = DatasetCreate(uuid = uuid4(), collected=datetime.now(), 
                        name = "test dataset", creator="Stephan",
                        keywords=["vP1 (mV)", "RF readout signal (mV)"],
                        ranking=0, scope_uuid= scope.uuid,
                        attributes={"Set-up" : "XLD"})
            
            dao_dataset.create(datasetCreate1, session)
            session.commit()
            datasetCreate2 = DatasetCreate(uuid = uuid4(), collected=datetime.now(), 
                        name = "test dataset", creator="Stephan",
                        keywords=["vP1 (mV)", "RF readout signal (mV)"],
                        ranking=0, scope_uuid= scope.uuid,
                        attributes={"Set-up" : "XLD"})
            
            dao_dataset.create(datasetCreate2, session)
            session.commit()

            ds = dao_dataset.read(datasetCreate1.uuid, session)
            
            self.assertEqual(ds.uuid, datasetCreate1.uuid)
            self.assertEqual(ds.alt_uid, datasetCreate1.alt_uid)
            self.assertEqual(ds.collected, datasetCreate1.collected)
            self.assertEqual(ds.name, datasetCreate1.name)
            self.assertEqual(ds.creator, datasetCreate1.creator)
            self.assertEqual(ds.keywords, datasetCreate1.keywords)
            self.assertEqual(ds.scope.uuid, scope.uuid)
            self.assertEqual(ds.attributes["Set-up"], datasetCreate1.attributes["Set-up"])
            
            du = DatasetUpdate(keywords=["vP1 (mV)", "RF readout signal (mV)", "vP2 (mV)"],
                attributes = {"Set-up" : "F006"})
            dao_dataset.update(ds.uuid, du, session)
            
            ds_updated = dao_dataset.read(datasetCreate1.uuid, session)
            self.assertEqual(ds_updated.keywords, du.keywords)

            dao_dataset.update(datasetCreate2.uuid, du, session)
            session.commit()

            dao_dataset.delete(datasetCreate1.uuid, session)
            session.commit()
            dao_dataset.delete(datasetCreate2.uuid, session)
            session.commit()
            _delete_scope(scope.uuid, session)

    def test_getting_attributes(self):
        with SessionLocal() as session:
            scope_1 = _create_scope("scope1", session)
            scope_2 = _create_scope("scope2", session)

            attr_project_1 = {"project" : "carpet"}
            attr_project_2 = {"project" : "6dot"}

            attr_setup_1 = {"set-up" : "XLD"}
            attr_setup_2 = {"set-up" : "F006"}
            attr_setup_3 = {"set-up" : "dipstick"}

            attr_sample_1 = {"sample" : "SQ0001"}
            attr_sample_2 = {"sample" : "SQ0002"}
            attr_sample_3 = {"sample" : "SQ0003"}

            datasets = []
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1 | attr_sample_1, session))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1 | attr_sample_1, session))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_3 | attr_sample_1, session))

            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1 | attr_sample_2, session))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1 | attr_sample_2, session))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_3 | attr_sample_2, session))

            datasets.append(_create_ds(scope_1, attr_project_2 | attr_setup_2 | attr_sample_3, session))
            datasets.append(_create_ds(scope_1, attr_project_2 | attr_setup_2 | attr_sample_3, session))
            datasets.append(_create_ds(scope_1, attr_project_2 | attr_setup_3 | attr_sample_3, session))

            out = dao_dataset.get_attributes(scope_1.uuid, {}, session)

            self.assertCountEqual(list(out.keys()), ['project', 'set-up', 'sample'])
            self.assertListEqual(out['project'], ["carpet", "6dot"])
            self.assertListEqual(out['set-up'], ["XLD", "dipstick", "F006"])
            self.assertListEqual(out['sample'], ["SQ0001", "SQ0002", "SQ0003"])

            out = dao_dataset.get_attributes(scope_1.uuid, {'project' : ["carpet"]}, session)

            self.assertCountEqual(list(out.keys()), ['project', 'set-up', 'sample'])
            self.assertListEqual(out['project'], ["carpet"])
            self.assertListEqual(out['set-up'], ["XLD", "dipstick"])
            self.assertListEqual(out['sample'], ["SQ0001", "SQ0002"])
            out = dao_dataset.get_attributes(scope_1.uuid, {'project' : ["carpet"], "set-up" :[ "XLD"]}, session)

            self.assertCountEqual(list(out.keys()), ['project', 'set-up', 'sample'])
            self.assertListEqual(out['project'], ["carpet"])
            self.assertListEqual(out['set-up'], ["XLD"])
            self.assertListEqual(out['sample'], ["SQ0001", "SQ0002"])

            out = dao_dataset.get_attributes(scope_1.uuid, {'project' : ["carpet"], "set-up" :[ "XLD", "dipstick"]}, session)

            self.assertCountEqual(list(out.keys()), ['project', 'set-up', 'sample'])
            self.assertListEqual(out['project'], ["carpet"])
            self.assertListEqual(out['set-up'], ["XLD", "dipstick"])
            self.assertListEqual(out['sample'], ["SQ0001", "SQ0002"])

            for ds in datasets:
                dao_dataset.delete(ds.uuid, session)
                session.commit()
                
            _delete_scope(scope_1.uuid, session)
            _delete_scope(scope_2.uuid, session)

    def test_distinct_dates(self):
        with SessionLocal() as session:
            scope_1 = _create_scope("scope1", session)
            scope_2 = _create_scope("scope2", session)

            attr_project_1 = {"project" : "carpet"}
            attr_project_2 = {"project" : "6dot"}

            attr_setup_1 = {"set-up" : "XLD"}
            attr_setup_2 = {"set-up" : "F006"}

            datasets = []
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1, session, datetime(2023, 1, 1, 1, 20, 0)))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1, session, datetime(2023, 1, 1, 1, 30, 0)))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1, session, datetime(2023, 1, 1, 1, 40, 0)))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_2, session, datetime(2023, 1, 2, 1, 20, 0)))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_2, session, datetime(2023, 1, 2, 1, 20, 10)))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_2, session, datetime(2023, 2, 2, 1, 20, 10)))
            datasets.append(_create_ds(scope_2, attr_project_2 | attr_setup_2, session, datetime(2023, 1, 3, 1, 20, 0)))
            datasets.append(_create_ds(scope_2, attr_project_2 | attr_setup_2, session, datetime(2023, 1, 4, 1, 20, 10)))
            datasets.append(_create_ds(scope_2, attr_project_2 | attr_setup_2, session, datetime(2023, 2, 5, 1, 20, 10)))

            datasetDistinctDates = DatasetSelection(scope_uuids=[scope_1.uuid, scope_2.uuid])
            dates = dao_dataset.get_distinct_dates(datasetDistinctDates, session)

            self.assertListEqual(dates, ['2023-01-01', '2023-01-02', '2023-02-02', '2023-01-03', '2023-01-04', '2023-02-05'])

            datasetDistinctDates = DatasetSelection(scope_uuids=[scope_1.uuid])
            dates = dao_dataset.get_distinct_dates(datasetDistinctDates, session)
            self.assertListEqual(dates, ['2023-01-01', '2023-01-02', '2023-02-02'])
            
            datasetDistinctDates = DatasetSelection(scope_uuids=[scope_1.uuid], attributes={'project': ['carpet'], 'set-up': ["XLD"]})
            dates = dao_dataset.get_distinct_dates(datasetDistinctDates, session)
            self.assertListEqual(dates, ['2023-01-01'])

            datasetDistinctDates = DatasetSelection(scope_uuids=[scope_1.uuid], attributes={'project': ['carpet'], 'set-up': ["XLD", "F006"]})
            dates = dao_dataset.get_distinct_dates(datasetDistinctDates, session)
            self.assertListEqual(dates, ['2023-01-01', '2023-01-02', '2023-02-02'])

            datasetDistinctDates = DatasetSelection(scope_uuids=[scope_1.uuid], attributes={'project': ['carpet2']})
            dates = dao_dataset.get_distinct_dates(datasetDistinctDates, session)
            self.assertListEqual(dates, [])

            for ds in datasets:
                dao_dataset.delete(ds.uuid, session)
                session.commit()
                
            _delete_scope(scope_1.uuid, session)
            _delete_scope(scope_2.uuid, session)

    def test_search(self):
        with SessionLocal() as session:
            scope_1 = _create_scope("scope1", session)

            attr_project_1 = {"project" : "carpet"}
            attr_project_2 = {"project" : "6dot"}

            attr_setup_1 = {"set-up" : "XLD"}
            attr_setup_2 = {"set-up" : "F006"}

            datasets = []
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1, session, datetime(2023, 1, 1, 1, 20, 0), name = "dataset 1234"))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1, session, datetime(2023, 1, 1, 1, 30, 0), name = "dataset 1234"))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_1, session, datetime(2023, 1, 1, 1, 40, 0), name = "dataset 124"))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_2, session, datetime(2023, 1, 2, 1, 20, 0), name = "dataset 1"))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_2, session, datetime(2023, 1, 2, 1, 20, 10), name = "dataset 14"))
            datasets.append(_create_ds(scope_1, attr_project_1 | attr_setup_2, session, datetime(2023, 2, 2, 1, 20, 10), name = "dataset 134"))
            datasets.append(_create_ds(scope_1, attr_project_2 | attr_setup_2, session, datetime(2023, 1, 3, 1, 20, 0), name = "dataset 123"))
            datasets.append(_create_ds(scope_1, attr_project_2 | attr_setup_2, session, datetime(2023, 1, 4, 1, 20, 10), name = "dataset 134"))
            datasets.append(_create_ds(scope_1, attr_project_2 | attr_setup_2, session, datetime(2023, 2, 5, 1, 20, 10), name = "dataset 124"))
            
            datasetSearch = DatasetSearch(scope_uuids=[scope_1.uuid], search_query="dataset")
            out = dao_dataset.search(datasetSearch, session)
            self.assertEqual(len(datasets), len(out))
            
            datasetSearch = DatasetSearch(scope_uuids=[scope_1.uuid], search_query="dataset 12")
            out = dao_dataset.search(datasetSearch, session)
            self.assertEqual(5, len(out))
            
            datasetSearch = DatasetSearch(scope_uuids=[scope_1.uuid], search_query="dataset 12",
                                          start_date=datetime(2023, 1, 1, 1, 0, 0), end_date=datetime(2023,1,2,0,0))
            out = dao_dataset.search(datasetSearch, session)
            self.assertEqual(3, len(out))
            
            datasetSearch = DatasetSearch(scope_uuids=[scope_1.uuid], search_query="dataset",
                                          start_date=datetime(2023, 1, 1, 1, 0, 0), end_date=datetime(2023,2,1,0,0))
            out = dao_dataset.search(datasetSearch, session)
            self.assertEqual(7, len(out))
            
            datasetSearch = DatasetSearch(scope_uuids=[scope_1.uuid], search_query="dataset",
                                          start_date=datetime(2023, 1, 1, 1, 0, 0), end_date=datetime(2023,2,1,0,0), attributes={"project" : ["6dot"]})
            out = dao_dataset.search(datasetSearch, session)
            self.assertEqual(2, len(out))
            
            for ds in datasets:
                dao_dataset.delete(ds.uuid, session)
                session.commit()
                
            _delete_scope(scope_1.uuid, session)
            
def _create_scope(name, session):
    create_obj = ScopeCreate(name = name, uuid=uuid4(), description="test-scope")
    dao_scope.create(create_obj, session)
    session.commit()
    return create_obj

def _delete_scope(scope_uuid, session):
    dao_scope.delete(scope_uuid, session)
    session.commit()

def _create_ds(scope, attr, session, collected = datetime.now(), name = "test dataset"):
    datasetCreate1 = DatasetCreate(uuid = uuid4(), collected=collected, 
                        name = name, creator="Anonymous",
                        keywords=["vP1 (mV)", "RF readout signal (mV)"],
                        ranking=0, scope_uuid= scope.uuid,
                        attributes=attr)
    
    dataset = dao_dataset.create(datasetCreate1, session)
    session.commit()
    return dataset

if __name__ == '__main__':
    # from etiket.db.get_db_session import SessionLocal, engine
    # from etiket.db.models import *

    # Base.metadata.create_all(engine)

    unittest.main()