from foobar import FoobarChildClass
"""
    This script is used to test the Classes and methods from foobar.py file
"""

# Test code
read_path = 'student_responses.csv'
write_path = 'final_scores.csv'
#initialize class
test_run = FoobarChildClass(read_path, write_path)
row_list = test_run.read_data()
# to be sent to write functio
final_result_list = []

# Loop through the rows in csv and extract expected results
for row in row_list:
    student_response = row[0].split(",")
    # perform checks for duplicates and test data
    if test_run.check_each_row(student_response):
        # extract everything aasides the email
        student_card = student_response[:-1]
        # call the transform_card_order_to_string function using self
        student_card_str = test_run.transform_card_order_to_string(student_card)
        # call the levensthein function on the string to get score
        lev_score = test_run.levenshtein_score(student_card_str)
        # compute score and percentage
        raw_score, perc = test_run.compute_score(len(student_card_str), lev_score)
        # append res to final_result_list
        final_result_list.append([student_response[-1], raw_score, perc])
        

# write the list to csv
test_run.write_student_scores(final_result_list)


# Get the mean and std.dev and print
mean_std = test_run.avg_and_sd()

"""
Things to note:
These script assume that there are no typographical errors i.e("palptine@council.org" != "palpatine@council.org")

"""
