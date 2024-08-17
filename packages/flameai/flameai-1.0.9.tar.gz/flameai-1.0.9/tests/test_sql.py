from flameai.sql import SQLConnect
from flameai.util import gen_abspath
import pandas as pd


def test_create_table():
    sc = SQLConnect()
    df = pd.DataFrame({'a': ['a', 'b', 'c', 'a', 'b', 'c'],
                       'b': [1, 2, 3, 2, 1, 0]})
    sc.create_table(table_name='table_a', df=df)
    result = sc.sql('select a, b from table_a')
    sc.delete_database()

    assert result['a'].to_list() == ['a', 'b', 'c', 'a', 'b', 'c']
    assert result['b'].to_list() == [1, 2, 3, 2, 1, 0]


def test_create_table_with_csv():
    sc = SQLConnect()
    csv_path = gen_abspath('./data', 'student.csv')
    sc.create_table_with_csv(table_name='table_student',
                             csv_path=csv_path,
                             sep='\t')
    result = sc.sql('select time, name, score, age from table_student')
    sc.delete_database()

    assert result['time'].to_list() == ['2023-12-16 17:23:00',
                                        '2023-12-16 17:24:00',
                                        '2023-12-16 17:25:00']
    assert result['name'].to_list() == ['John Smith', 'Emily Johnson', 'Michael Brown']
    assert result['score'].to_list() == [99.50, 83.00, 55.00]
    assert result['age'].to_list() == [18, 23, 23]


def test_table_join():
    sc = SQLConnect()
    student_path = gen_abspath('./data', 'student.csv')
    course_path = gen_abspath('./data', 'course.csv')
    sc.create_table_with_csv(table_name='table_student',
                             csv_path=student_path,
                             sep='\t')
    sc.create_table_with_csv(table_name='table_course',
                             csv_path=course_path,
                             sep='\t')
    query = """
    SELECT
        a.name,
        a.age,
        b.course
    FROM table_student a
    LEFT JOIN table_course b
    ON a.name = b.name
    """
    result = sc.sql(query)
    sc.delete_database()

    assert result['name'].to_list() == ['John Smith'] * 4 + ['Emily Johnson'] * 3 + \
        ['Michael Brown'] * 3
    assert result['age'].to_list() == [18, 18, 18, 18, 23, 23, 23, 23, 23, 23]
    assert result['course'].to_list() == ['Art', 'Design', 'English', 'Geography',
                                          'English', 'History', 'Music', 'Computing',
                                          'English', 'Technology']
