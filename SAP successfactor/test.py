class Model_GroupFilters_HRIS_Element:
    filter_type = ''
    element_reference = ''
    effective_date = ''
    field_id = ''
    reference_field = ''

# Create a list of objects for Model_GroupFilters_HRIS_Element
filters = []

# Creating objects and setting attributes directly
filter1 = Model_GroupFilters_HRIS_Element()
filter1.filter_type = 'status'
filter1.element_reference = 'employee_status (emp stat)'
filter1.effective_date = '2024-01-01'
filter1.field_id = '001'
filter1.reference_field = 'active'
filters.append(filter1)

filter2 = Model_GroupFilters_HRIS_Element()
filter2.filter_type = 'department'
filter2.element_reference = 'department_code (dpt code)'
filter2.effective_date = '2024-02-01'
filter2.field_id = '002'
filter2.reference_field = 'HR'
filters.append(filter2)

filter3 = Model_GroupFilters_HRIS_Element()
filter3.filter_type = 'location'
filter3.element_reference = 'office_location (off loc)'
filter3.effective_date = '2024-03-01'
filter3.field_id = '003'
filter3.reference_field = 'NYC'
filters.append(filter3)

filter4 = Model_GroupFilters_HRIS_Element()
filter4.filter_type = 'role'
filter4.element_reference = 'job_role (jr)'
filter4.effective_date = '2024-04-01'
filter4.field_id = '004'
filter4.reference_field = 'manager'
filters.append(filter4)

filter5 = Model_GroupFilters_HRIS_Element()
filter5.filter_type = 'employment_type'
filter5.element_reference = 'employment_type_code (emp code)'
filter5.effective_date = '2024-05-01'
filter5.field_id = '005'
filter5.reference_field = 'full_time'
filters.append(filter5)

print(filters[0].element_reference[:filters[0].element_reference.find("(")-1])