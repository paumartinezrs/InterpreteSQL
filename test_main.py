import sequel 
import pandas as pd

def test_select_estrella_basico():
    expected = pd.read_csv(f"./data/jobs.csv")
    assert expected.equals(sequel.ejecuta("select * from jobs"))

def test_select_columna():
    expected = pd.read_csv(f"./data/jobs.csv")
    expected = expected[["job_id"]]
    assert expected.equals(sequel.ejecuta("select job_id from jobs"))

def test_select_columnas():
    expected = pd.read_csv(f"./data/jobs.csv")
    expected = expected[["job_id", "job_title"]]
    assert expected.equals(sequel.ejecuta("select job_id, job_title from jobs"))

def test_select_columna_calculada():
    expected = pd.read_csv(f"./data/jobs.csv")
    expected["new"] = expected["job_id"]*2.0
    expected = expected[["new"]]
    assert expected.equals(sequel.ejecuta("select job_id*2 as new from jobs"))

def test_select_columna_calculada_prioridad_operadores():
    expected = pd.read_csv(f"./data/jobs.csv")
    expected["new"] = expected["job_id"]+1.0
    expected = expected[["new"]]*2
    assert expected.equals(sequel.ejecuta("select (job_id + 1)*2 as new from jobs"))

def test_order_by():
    expected = pd.read_csv(f"./data/countries.csv")
    expected = expected.sort_values(by = ["region_id", "country_name"], ascending = [True, False])
    assert expected.equals(sequel.ejecuta("select * from countries order by region_id, country_name desc"))


