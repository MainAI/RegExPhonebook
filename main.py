import csv
import re


def read_write(switch, file, name_list=None):
    """ switch = 1 for read .csv; switch = 2 for write .csv """
    if name_list is None:
        name_list = []
    if switch == 1:
        with open(file, encoding="UTF-8") as f:
            rows = csv.reader(f, delimiter=",")
            name_list = list(rows)
            return name_list
    elif switch == 2:
        with open(file, "w", encoding="UTF-8", newline="") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(name_list)
            return


def sort_by_rex(person_list):
    """
    use regular expressions to find full name and phone number
    other item find by index in list
    return: double_list is result list without merge double data
    """
    double_list = [person_list[0]]
    for person_info in person_list[1:]:
        organization = person_info[3]
        position = person_info[4]
        phone = person_info[5]
        email = person_info[-1]

        temp_str = ",".join(person_info)
        pattern_word_surname = r"(^\w*)[ ,]?(\w*)[ ,]?(\w*)"
        temp_fullname = re.search(pattern_word_surname, temp_str)
        lastname = temp_fullname.group(1)
        firstname = temp_fullname.group(2)
        surname = temp_fullname.group(3)

        pattern_tel_number = r"(\+7|8)\s*\(?(\d{3})[ \)-]*(\d{3})[ -]*(\d{2})"\
            r"[ -]?(\d{2})[ ]?[а-я]*[ .\(]*[а-я]*[. ]*(\d{4})*\)?"
        temp_phone = re.search(pattern_tel_number, phone)
        if temp_phone is not None:
            if temp_phone.group(6) is None:
                substitution = r"+7(\2)\3-\4-\5"
            else:
                substitution = r"+7(\2)\3-\4-\5 доб.\6"
            temp_phone = re.sub(pattern_tel_number, substitution, phone)
        else:
            temp_phone = ""
        result = [lastname, firstname, surname, organization, position, temp_phone, email]
        double_list.append(result)
    return double_list


def double_free(list_modify):
    """
    Create dictionary with key = lastname, firstname; merge value with same key by data with same list index.
    :param list_modify: list with double data
    :return: double_free_list
    """
    dict_data = {}
    for info in list_modify:
        key = tuple(info[:2])
        if dict_data.get(key) is None:
            dict_data[key] = []
        index_ = 0
        for item in info:
            value_list = dict_data[key]
            if index_ < len(dict_data.get(key)):
                if value_list[index_] == "":
                    value_list[index_] = item
                    index_ += 1
                else:
                    index_ += 1
            else:
                value_list.append(item)
                index_ += 1
    double_free_list = list(dict_data.values())
    return double_free_list


if __name__ == "__main__":
    contacts_list = read_write(1, "phonebook_raw.csv")
    list_test = sort_by_rex(contacts_list)
    result_phonebook = double_free(list_test)
    read_write(2, "phonebook.csv", result_phonebook)
