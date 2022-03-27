import os
import sys
import psycopg2
from psycopg2 import Error



try:
    connection = psycopg2.connect(user="sys.argv[0]",
                                  password="sys.argv[1]",
                                  host="sys.argv[2]",
                                  port="5432",
                                  database="sys.argv[3]")

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = ''' CREATE TABLE IF NOT EXISTS public.division_store_master
(
    division_store_id INTEGER NOT NULL PRIMARY KEY,
	division_id VARCHAR(5) NOT NULL,
    store_id VARCHAR(5) NOT NULL,
	brand_name VARCHAR(50) NOT NULL,
	address VARCHAR(100) NOT NULL,
	store_type VARCHAR(50) NOT NULL,
	timezone VARCHAR(3) NOT NULL,
	fac_type VARCHAR(50) NOT NULL,
	active VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.store_aisle_master
(
    store_aisle_id INTEGER NOT NULL PRIMARY KEY,
    division_store_id INTEGER NOT NULL,
	aisle_no VARCHAR(4) NOT NULL,
	aisle_active VARCHAR(1) NOT NULL,
	aisle_type VARCHAR(50) NOT NULL,
	CONSTRAINT division_store_id
      FOREIGN KEY(division_store_id) 
	  REFERENCES public.division_store_master(division_store_id)
);

CREATE TABLE IF NOT EXISTS public.usecase_master
(
    usecase_id INTEGER NOT NULL PRIMARY KEY,
    usecase_name VARCHAR(50) NOT NULL,
	usecase_desc VARCHAR(100) NOT NULL,
	active VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.screen_master
(
    screen_id INTEGER NOT NULL PRIMARY KEY,
    screen_name VARCHAR(50) NOT NULL,
	usecase_id INTEGER NOT NULL,
	active VARCHAR(1) NOT NULL,
	CONSTRAINT fk_usecase_id
      FOREIGN KEY(usecase_id) 
	  REFERENCES public.usecase_master(usecase_id)
);
	
	
	CREATE TABLE IF NOT EXISTS public.screen_master
(
    screen_id INTEGER NOT NULL PRIMARY KEY,
    screen_name VARCHAR(50) NOT NULL,
	usecase_id INTEGER NOT NULL,
	active VARCHAR(1) NOT NULL,
	CONSTRAINT fk_usecase_id
      FOREIGN KEY(usecase_id) 
	  REFERENCES public.usecase_master(usecase_id)
);

CREATE TABLE IF NOT EXISTS public.workflow_master
(
    workflow_id INTEGER NOT NULL PRIMARY KEY,
    workflow_name VARCHAR(50) NOT NULL,
	workflow_desc VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.priority_master
(
    priority_id INTEGER NOT NULL PRIMARY KEY,
    priority_name VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.reasons_master
(
    reason_id INTEGER NOT NULL PRIMARY KEY,
    reason_desc VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.shift_timings_master
(
    shift_id INTEGER NOT NULL PRIMARY KEY,
    shift_name VARCHAR(50) NOT NULL,
	shift_start_time TIMESTAMP NOT NULL,
	shift_end_time TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS public.hand_off_checklist_questions
(
    checklist_question_id INTEGER NOT NULL PRIMARY KEY,
    checklist_question VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS public.hand_off_checklist_shift_questions_mapping
(
    checklist_shift_question_id INTEGER NOT NULL PRIMARY KEY,
	shift_id INTEGER REFERENCES shift_timings_master(shift_id) NOT NULL,
    checklist_question_id INTEGER REFERENCES hand_off_checklist_questions(checklist_question_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.department_master
(
    department_id INTEGER NOT NULL PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.employee_master
(
	employee_id integer NOT NULL PRIMARY KEY,
	employee_name VARCHAR(100) NOT NULL, 
	euid VARCHAR NOT NULL,
	active VARCHAR(1) NOT NULL,
	division_store_id INTEGER REFERENCES division_store_master(division_store_id) NOT NULL
);


CREATE TABLE IF NOT EXISTS public.employee_details
(
    employee_details_id integer NOT NULL PRIMARY KEY,
	employee_id INTEGER REFERENCES employee_master(employee_id) NOT NULL,
    status VARCHAR(50) NOT NULL,
	available_date DATE NOT NULL,
	available_hours NUMERIC,
	shift_start_time TIMESTAMP NOT NULL,
	shift_end_time TIMESTAMP NOT NULL,
	department_id INTEGER REFERENCES department_master(department_id) NOT NULL,
	task_type_preference VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.employee_intermediate
(
	employee_intermediate_id INTEGER NOT NULL PRIMARY KEY,
	employee_detiid INTEGER REFERENCES employee_master(employee_id) NOT NULL,
	action_initiated VARCHAR(100) NOT NULL,
	activity_id VARCHAR NOT NULL,
	record_status VARCHAR(50) NOT NULL,
	work_flow_status VARCHAR(50) NOT NULL,
	created_by VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL,
	last_updated_by VARCHAR(100) NOT NULL,
	last_updated_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.images_master
(
	image_id INTEGER NOT NULL PRIMARY KEY,
	image BYTEA,
	created_by VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.store_scheduled_truck_details
(
	truck_id INTEGER NOT NULL PRIMARY KEY,
	route_no VARCHAR(50) NOT NULL,
	scheduled_time TIMESTAMP NOT NULL,
	available_date DATE NOT NULL,
	product_type VARCHAR(50) NOT NULL,
	delivery_start_time TIMESTAMP NOT NULL,
	delivery_end_time TIMESTAMP NOT NULL,
	division_store_id INTEGER REFERENCES division_store_master(division_store_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.truck_arrivals_tracker
(
	arrival_id INTEGER NOT NULL PRIMARY KEY,
	truck_id INTEGER REFERENCES store_scheduled_truck_details(truck_id) NOT NULL,
	seal_no VARCHAR NOT NULL,
	freight_status VARCHAR(50) NOT NULL,
	arrived_time TIMESTAMP NOT NULL,
	activity_id VARCHAR NOT NULL,
	work_flow_status VARCHAR(50) NOT NULL,
	created_by VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL,
	last_updated_by VARCHAR(100) NOT NULL,
	last_updated_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.arrived_truck_images
(
	arrived_truck_image_id INTEGER NOT NULL PRIMARY KEY,
	arrival_id INTEGER REFERENCES truck_arrivals_tracker(arrival_id) NOT NULL,
	image_id INTEGER REFERENCES images_master(image_id) NOT NULL,
	comments_desc VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS public.store_inventory_details
(
	inventory_id INTEGER NOT NULL PRIMARY KEY,
	truck_id INTEGER REFERENCES store_scheduled_truck_details(truck_id) NOT NULL,
	store_aisle_id INTEGER REFERENCES store_aisle_master(store_aisle_id) NOT NULL,
	inventory_type VARCHAR(50) NOT NULL,
	measurement_type VARCHAR(20) NOT NULL,
	quantity INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS public.store_inventory_qty_changes_tracker
(
	inventory_changes_tracker_id INTEGER NOT NULL PRIMARY KEY,
	inventory_id INTEGER REFERENCES store_inventory_details(inventory_id) NOT NULL,
	previous_qty INTEGER NOT NULL,
	reason_id INTEGER REFERENCES reasons_master(reason_id) NOT NULL,
	created_by VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.hand_off_checklist_shift_questions_feedback
(
	checklist_feedback_id  INTEGER NOT NULL PRIMARY KEY,
	division_store_id INTEGER REFERENCES division_store_master(division_store_id) NOT NULL,
	checklist_shift_question_id INTEGER REFERENCES hand_off_checklist_shift_questions_mapping(checklist_shift_question_id) NOT NULL,
	checklist_value VARCHAR(20) NOT NULL,
	created_by VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL,
	last_updated_by VARCHAR(100) NOT NULL,
	last_updated_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.hand_off_checklist_shift_master_feedback
(
	checklist_master_feedback_id INTEGER NOT NULL PRIMARY KEY,
	division_store_id INTEGER REFERENCES division_store_master(division_store_id) NOT NULL,
	notes VARCHAR NOT NULL,
	submitted_timestamp TIMESTAMP NOT NULL,
	is_submitted VARCHAR(5) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.workflow_audit
(
	workflow_audit_id INTEGER NOT NULL PRIMARY KEY,
	activity_id VARCHAR NOT NULL,
	workflow_id INTEGER REFERENCES workflow_master(workflow_id) NOT NULL,
	request_processed_by_ms VARCHAR(1) NOT NULL,
	request_processed_by_orsolver VARCHAR(1) NOT NULL,
	data_merged_to_tasklist VARCHAR(1) NOT NULL,
	last_updated_by VARCHAR(100) NOT NULL,
	last_updated_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.tasks_master
(
	task_id INTEGER NOT NULL PRIMARY KEY,
	task_name VARCHAR(100) NOT NULL,
	task_status VARCHAR(50) NOT NULL,
	task_date DATE NOT NULL,
	timer_status VARCHAR(20) NOT NULL,
	time_stamp TIMESTAMP NOT NULL,
	truck_id INTEGER REFERENCES store_scheduled_truck_details(truck_id) NOT NULL,
	actual_time VARCHAR(5) NOT NULL,
	aisle_no VARCHAR(4) NOT NULL,
	aisle_preference VARCHAR(1) NOT NULL,
	display_quantity VARCHAR(50) NOT NULL,
	estimated_time VARCHAR(5) NOT NULL,
	finish NUMERIC NOT NULL,
	priority_id INTEGER REFERENCES priority_master(priority_id) NOT NULL,
	process VARCHAR(50) NOT NULL,
	reason VARCHAR NOT NULL,
	start_value NUMERIC NOT NULL,
	start_window TIMESTAMP NOT NULL,
	stocking_rate NUMERIC NOT NULL,
	employee_id INTEGER REFERENCES employee_master(employee_id) NOT NULL,
	division_store_id INTEGER REFERENCES division_store_master(division_store_id) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.tasks_intermediate
(
	tasks_intermediate_id INTEGER NOT NULL PRIMARY KEY,
	task_id INTEGER REFERENCES tasks_master(task_id) NOT NULL,
	task_status VARCHAR(50) NOT NULL,
	task_date DATE NOT NULL,
	timer_status VARCHAR(20) NOT NULL,
	employee_id INTEGER REFERENCES employee_master(employee_id) NOT NULL,
	actual_time VARCHAR(5) NOT NULL,
	activity_id VARCHAR NOT NULL,
	work_flow_status VARCHAR(50) NOT NULL,
	created_by VARCHAR(100) NOT NULL,
	created_date TIMESTAMP NOT NULL,
	last_updated_by VARCHAR(100) NOT NULL,
	last_updated_date TIMESTAMP NOT NULL

);'''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
