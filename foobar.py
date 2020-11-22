"""
Docstring for the class
"""
import csv
import numpy as np


class FoobarClass:

    def __init__(self):
        """
        Initialize the class
        :param name: The class name
        :param code_map: A dictionary that specifies how the card labels should be converted to letters
        :param answer: The correct ordering of cards (by their label) translated into a string according to the code map
        :param max_score: The highest possible score
        """
        self.name = "FoobarBaseClass"
        self.code_map = {'A1': 'a', 'A2': 'b', 'A3': 'c', 'A4': 'd', 'A5': 'e', 'A6': 'f', 'A7': 'g'}
        self.answer = 'abcde'
        self.max_score = 20

    def levenshtein_score(self, source_string):
        """
        Implementation of the Levenshtein Algorithm from Wikipedia article
        https://en.wikipedia.org/wiki/Levenshtein_distance

        Also known as the edit distance

        For example, the Levenshtein Distance between "the" and "there" is 2; the letters "r" and "e"
        must be added to change "the" into "there"

        :param source_string: the string to be compared to the answer
        :return the number of edits to match the source with the answer, i.e. the number of incorrect cards
        """
        if source_string == self.answer:
            return 0
        if len(source_string) == 0:
            return len(self.answer)
        if len(self.answer) == 0:
            return len(source_string)
        v0 = [i for i in range(len(self.answer) + 1)]
        v1 = [0] * (len(self.answer) + 1)

        for i in range(len(source_string)):
            v1[0] = i + 1
            for j in range(len(self.answer)):
                cost = 0 if source_string[i] == self.answer[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(self.answer)]

    def transform_card_order_to_string(self, card_order):
        """
        Turn a list of card labels into a string for measurement

        For example, [A1, A2, A3] would become 'abc' based on the code map

        :param card_order: the input list of card labels
        :return: output_string: the list converted to a string
        """
        output_string = str()
        for card in card_order:
            output_string += self.code_map[card]

        return output_string


        

class FoobarChildClass(FoobarClass):
    """
        A child class of Foobar tha inherits all its properties
        This is done according to the instructions
        1. Reads the csv data
        2. Scores the card sorting
        3. Writes the results for each student to a new CSV file
        4. Prints the average and standard deviation of the student raw scores
    """
    
    
    def __init__(self, read_path, write_path):
        FoobarClass.__init__(self)
        self.filepath_r = read_path # path to read file
        self.filepath_w = write_path # path to write file
        self.email_list = []
        self.scores_list = []
    
    def read_data(self):
        """
        1. Reads the csv data
        The data should be read from the csv file supplied
        """
        data_list = []
        
        with open(self.filepath_r, 'r',) as file:
            reader = csv.reader(file, delimiter = '\t')
            for row in reader:
                # read the data for each student
                data_list.append(row)
        return data_list

        

    def compute_score(self, str_len, lev_score):
        """
        2. Scores the card sorting
        Each correct card is worth 4 points.  Each incorrect card should subtract 1 point(Readme says 2 points).
        Scores less than zero should be scored as zero
        """
        # no. of cards minus lev_score i.e the number of incorrect cards
        correct_cards = str_len - lev_score

        # student final score
        final_score = (correct_cards * 4) - (lev_score * 2)
        # check for scores less than zero
        if final_score < 0:
            final_score = 0
        
        # calc score percentage
        stu_perc = round(final_score/20, 2)
        # add this score to the list of scores - will be used 
        # to calculate mean and std later
        self.scores_list.append(final_score)

        return final_score, stu_perc

    def write_student_scores(self, row_list):
        """
        3. Writes the results for each student to a new CSV file
        The output format of the csv file should be:
        <student id>, <raw score>, <percentage correct>
        """
        with open(self.filepath_w, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    def check_each_row(self, row):
        """
        This function performs checks on the emails for duplicte and test data
        """
        student_email = row[-1]
        # check for test email
        if student_email != "test@test.com":
            if student_email not in self.email_list:
                # add the email to the list
                self.email_list.append(student_email)
                return True
        return False
    
    def avg_and_sd(self):
        """
        4. Prints the average and standard deviation of the student raw scores
        """
        mean = round(np.mean(self.scores_list), 2)
        std = round(np.std(self.scores_list), 2)
        
        # print results
        print ({"mean": mean, "std_dev": std})
