from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import json
import sys


@dataclass
class Tools:
    browser: webdriver
    url = 'https://reseau-ges.percipio.com'

    def connection(self, usr: str, pwd: str) -> bool:
        # On dit au navigateur d'aller sur l'url suivant
        self.browser.get('https://reseau-ges.percipio.com/login')

        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.ID, "loginName")))

        # type text
        text_area = self.browser.find_element(By.ID, "loginName")
        text_area.send_keys(usr)

        # click submit button
        next_btn = self.browser.find_element(By.XPATH, "//button[@class='Button---root---2BQqW Button---primary---1O3lq "
                                                      "Button---small---3PMLN Button---center---13Oaw']")
        next_btn.click()

        sleep(1)

        # type text
        text_area = self.browser.find_element(By.ID, "password")
        text_area.send_keys(pwd)

        # click submit button
        submit_button = self.browser.find_element(By.XPATH, "//button[@class='Button---root---2BQqW "
                                                           "Button---primary---1O3lq Button---small---3PMLN "
                                                           "Button---center---13Oaw']")
        submit_button.click()

        sleep(5)

        return True

    def check_exists_by_xpath(self, xpath) -> bool:
        try:
            self.browser.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def go_to_assignement(self) -> bool:
        self.browser.get('https://reseau-ges.percipio.com/assignments')

        return True

    def get_all_cours(self):
        btn_show_detail = self.browser.find_elements(By.XPATH,
            "//button[@class='Button---root---2BQqW Button---flat---fb6Ta Button---medium---1CC5_ Button---center---13Oaw']")

        for btn in btn_show_detail:
            btn.click()
            sleep(1)

        a_courses = self.browser.find_elements(By.TAG_NAME, "a")

        courses = []
        for a in a_courses:
            if 'courses' in a.get_attribute('href'):
                courses.append(a.get_attribute('href'))
        return courses
    
    def get_all_videos(self, course):
        sleep(2)
        a_videos = self.browser.find_elements(By.TAG_NAME, "a")
        
        videos = []
        for a in a_videos:
            try:
                link = a.get_attribute('href')
                if '/videos' in link and course in link:
                    if link not in a_videos:
                        videos.append(a.get_attribute("href"))
            except:
                pass
        return videos

    def get_cours(self, course_url: str) -> None:
        self.browser.get(course_url)

    def get_video(self, video_url: str):
        self.browser.get(video_url)

    def get_videos(self, video_id: str) -> None:
        self.browser.get(self.url + '/videos/' + video_id)

    def launch_video(self) -> None:
        # Lancement de la vidéo
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'playbackTooltip')))
        except TimeoutException:
            sys.exit("Loading took too much time!")

        play = self.browser.find_element(By.ID, 'playbackTooltip')

        play.click()

        sleep(1)

        # Gotta go fast
        self.browser.find_element(By.ID, 'video-player-settings-button').click()

        sleep(0.5)

        self.browser.find_element(By.ID, 'speed').click()

        sleep(0.5)

        speed_2 = self.browser.find_element(By.XPATH, "//span[@id='current_value_prefix'][text()='2']")

        speed_2.click()

    def get_completion_status(self) -> bool:
        div_completion_all = self.browser.find_element(By.XPATH, "//div[@class='ProgressBar---trail---3y2hW']")

        div_completion_status = self.browser.find_element(By.XPATH, "//div[@class='ProgressBar---stroke---1w8-k']")

        total_width = div_completion_all.value_of_css_property('width')

        actual_width = div_completion_status.value_of_css_property('width')

        return actual_width == total_width

    def check_for_test(self) -> str:
        link_to_test = ''
        try:
            WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@class='Button---root---2BQqW Button---primary---1O3lq Button---medium---1CC5_ Button---center---13Oaw']")))
            test_btn = self.browser.find_element(By.XPATH, "//a[@class='Button---root---2BQqW Button---primary---1O3lq Button---medium---1CC5_ Button---center---13Oaw']")
            return test_btn.get_attribute('href')
        except:
            return link_to_test
            
    def passing_test(self) -> bool:
        print("Début du Test")

        sleep(2)

        # Checking si déja passé
        if self.test_is_passed() is False:

            sleep(2)

            # Si test en cours continue
            if self.check_exists_by_xpath("//a[@id='assessment-continue']"):
                btn_launch = self.browser.find_element(By.XPATH, "//a[@id='assessment-continue']")
                
            # Sinon nouveau test
            elif self.check_exists_by_xpath("//button[@class='Button---root---2BQqW Button---primary---1O3lq Button---"
                                            "small---3PMLN Button---center---13Oaw']"):
                btn_launch = self.browser.find_element(By.XPATH, 
                    "//button[@class='Button---root---2BQqW Button---primary--"
                    "-1O3lq Button---small---3PMLN Button---center---13Oaw']")
            else:
                btn_launch = self.browser.find_element(By.XPATH, "//button[@class='Button---root---2BQqW "
                                                                "Button---primary---1O3lq Button---small---3PMLN "
                                                                "Button---center---13Oaw']")
            btn_launch.click()

            sleep(2)

            end_test = False

            while not end_test:

                sleep(2)

                course_title = self.browser.find_element(By.XPATH, "//h1[@class='PageHeading---title---A09FC']").text

                question = self.browser.find_element(By.XPATH, "//div[@class='QuestionMessages---stem---2uUKi']").text
            
                instruction = (self.browser.find_element(By.XPATH, 
                    "//div[@class='MessageBar---instruction---3-J99']").text).strip()

                advancement = self.browser.find_element(By.XPATH, "//p[@class='PageHeading---subtitle---qkcIk']").text

                # calcul de l'avancement

                current_question_pos_start = advancement.index(' ')

                current_question_pos_end = advancement.index(' ', current_question_pos_start + 1)

                current_question = advancement[current_question_pos_start + 1: current_question_pos_end]

                max_question_pos_start = advancement.index('of ')

                max_question = advancement[max_question_pos_start + len('of '):]

                end_test = max_question == current_question

                with open("test_answer.json", "r") as jsonFile:
                    test_answer = json.load(jsonFile)

                # Si le cours n'est pas connu dans le fichier de réponse
                # On ajoute le titre du cours à notre fichier de réponse
                if course_title not in test_answer:
                    test_answer[course_title] = {}

                # Si la question n'est pas connu dans le cours
                # On l'ajoute au cours
                if question not in test_answer[course_title]:
                    test_answer[course_title][question] = None

                answer_input_id = test_answer[course_title][question]

                # Si la réponse est pas encore connu
                if answer_input_id is None:
                    # Appel de la bonne question en fonction de l'instruction
                    if instruction == "Instruction: Choose all options that best answer the question.":
                        test_answer[course_title][question] = self.find_answer_checkbox()

                    elif instruction == "Instruction: Choose the option that best answers the question.":
                        test_answer[course_title][question] = self.find_answer_radio_button()
                        print()
                    elif instruction == "Instruction: Rank the following items in the correct sequence, by dragging with your mouse or finger. If using a keyboard, Tab between items, press Space Bar to pick up, Arrow keys to move, Space Bar to drop.":
                        test_answer[course_title][question] = self.find_answer_order()

                    elif instruction == "Instruction: For each option, select all the answer choices that apply.":
                        test_answer[course_title][question] = self.find_associated_answer()
                    elif instruction == "Instruction: For each option, select the best answer choice.":
                        test_answer[course_title][question] = self.find_associated_answer_radio()
                    # Par défaut
                    else:
                        print(instruction)
                        print("Réponse pas encore gérée")
                        exit(0)

                # Si on connait la réponse
                else:
                    # Appel de la bonne question en fonction de l'instruction
                    if instruction == "Instruction: Choose all options that best answer the question.":
                        self.click_answer_checkbox(answer_input_id)

                    elif instruction == "Instruction: Choose the option that best answers the question.":
                        self.click_answer_radio_button(answer_input_id)

                    elif instruction == "Instruction: Rank the following items in the correct sequence, by dragging with your mouse or finger. If using a keyboard, Tab between items, press Space Bar to pick up, Arrow keys to move, Space Bar to drop.":
                        self.click_answer_order(answer_input_id)

                    elif instruction == "Instruction: For each option, select all the answer choices that apply.":
                        self.click_associated_answer(answer_input_id)
                        
                    elif instruction == "Instruction: For each option, select the best answer choice.":
                        test_answer[course_title][question] = self.click_associated_answer(answer_input_id)
                    # Par défaut
                    else:
                        print("Réponse pas encore gérée")
                        exit(0)

                # On enregistre dans le json
                with open("test_answer.json", "w") as jsonFile:
                    json.dump(test_answer, jsonFile)

                if end_test:
                    self.browser.find_element(By.XPATH, "//a[@class='Button---root---2BQqW Button---primary---1O3lq "
                                                       "Button---small---3PMLN Button---center---13Oaw']").click()
                else:
                    self.browser.find_element(By.XPATH, 
                        "//button[@class='Button---root---2BQqW Button---primary---1O3lq "
                        "Button---small---3PMLN Button---center---13Oaw']").click()

            sleep(4)

            test_passed = self.test_is_passed()
            if test_passed is False:
                self.passing_test()

        print("Fin du test")

        return True

    def find_answer_radio_button(self) -> str:
        input_class = "RadioButton---input---3iHUk"

        # Un element cache l'input donc on va clicker sur l'element au dessus
        elem_to_click = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='" + input_class + "']/following-sibling::span")))
        elem_to_click.click()

        # On valide la réponse

        verify_button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='Question---verifyButton---KIKC0'] | //div[@class='Question---nextButton---oEnX1']")))
        verify_button.click()
            

        # On récupère la bonne réponse
        good_answer_div = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='Question---option---UEIWm Question---correct---HaOFo']")))
        good_answer_input = good_answer_div.find_element(By.TAG_NAME, "input")
        id_good_answer = good_answer_input.get_attribute('id')
        return id_good_answer

    def click_answer_radio_button(self, id_answer):
        # On prend le bon input
        # Un element cache l'input donc on va clicker sur l'element au dessus
        elem_to_click = self.browser.find_element(By.XPATH, "//input[@id='" + id_answer + "']/following-sibling::span")

        elem_to_click.click()

        sleep(2)

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

        # On récupère la bonne réponse
        div_good_answer = self.browser.find_element(By.XPATH, "//div[@class='Question---option---UEIWm "
                                                             "Question---correct---HaOFo']")

        input_good_answer = div_good_answer.find_element(By.XPATH, "//input[@class='RadioButton---input---3iHUk']")

        id_good_answer = input_good_answer.get_attribute('id')
        
        return id_good_answer

    def find_answer_checkbox(self) -> list:
        input_class = "Checkbox---input---e73Wy Checkbox---labelledInputCheckbox---2oIZ5"

        # On prend le premier input
        # Un element cache l'input donc on va clicker sur l'element au dessus
        elem_to_click = self.browser.find_element(By.XPATH, "//input[@class='" + input_class + "']/following-sibling"
                                                                                              "::span")
        elem_to_click.click()

        sleep(2)

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

        div_good_answers = self.browser.find_elements(By.XPATH, "//div[@class='Question---option---UEIWm Question---multichoiceCheckboxes---3HsIj Question---correct---HaOFo']")

        list_id_answers = []

        for div_good_answer in div_good_answers:
            input_good_answer = div_good_answer.find_element(By.TAG_NAME, "input")

            id_good_answer = input_good_answer.get_attribute('id')
            list_id_answers.append(id_good_answer)

        return list_id_answers

    def click_answer_checkbox(self, list_id_answer):
        for id_answer in list_id_answer:
            # On prend le bon input
            # Un element cache l'input donc on va clicker sur l'element au dessus
            elem_to_click = self.browser.find_element(By.XPATH, "//input[@id='" + id_answer + "']"
                                                                                             "/following-sibling::span")

            elem_to_click.click()

            sleep(1.2)

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

    def find_answer_order(self):
        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

        # On récupère les réponses dans l'ordre
        ol_answer = self.browser.find_element(By.XPATH, "//ol[@class='DraggableList---root---fLcK8']")

        lis_answer = ol_answer.find_elements(By.TAG_NAME, 'li')

        pos = 1

        answer_order = {}

        for li_answer in lis_answer:

            content = li_answer.text
            answer = content[:content.index("\n")]

            if "Correct answer." in content:
                answer_order[pos] = answer
                pos += 1
            else:
                pos_answer_corrected_in_text = content.index("This should be number ")
                pos_answer_corrected = content[pos_answer_corrected_in_text +
                                               len("This should be number "):len(content) - 1].split(' ')[0]
                answer_order[int(pos_answer_corrected)] = answer

        return answer_order

    def click_answer_order(self, answer_order):
        key_sorted = sorted(answer_order.keys())

        for answer in key_sorted:
            lis_answer = self.browser.find_elements(By.XPATH, "//ol[@class='DraggableList---root---fLcK8']//li")
            sleep(1)

            nbr_tab = 1

            for li in lis_answer:
                if li.text == answer_order[answer]:
                    if nbr_tab > int(answer):
                        while nbr_tab > int(answer):
                            actions = ActionChains(self.browser)
                            actions.drag_and_drop_by_offset(li, 0, -50).perform()
                            sleep(1)

                            nbr_tab -= 1
                    else:
                        while nbr_tab < int(answer):
                            actions = ActionChains(self.browser)
                            actions.drag_and_drop_by_offset(li, 0, 50).perform()
                            sleep(1)

                            nbr_tab += 1

                nbr_tab += 1

            sleep(2)

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

    def find_associated_answer(self):
        result_to_return = {}

        self.browser.find_element(By.XPATH, "//div[@class='Checkbox---inputCheckbox---3Yadt']").click()

        sleep(1)

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

        # On récupère toutes les options
        options = self.browser.find_element(By.XPATH, "//ul[@class='Matching---ul---bIrQZ']")

        dict_letter_answer = {}

        for li in options.find_elements(By.XPATH, "//li[@class='Matching---option---1L906']"):
            content = li.text

            letter = content[:content.index(':')]

            answer = content[content.index(':') + 1:]

            dict_letter_answer[letter] = answer

        matching_choices = self.browser.find_elements(By.XPATH, "//fieldset")

        for div in matching_choices:
            title = div.text[:div.text.index('\n')]

            result_to_return[title] = []
            if 'Incorrect answers' in div.text:
                try:
                    correct_answer = div.text[div.text.index("Incorrect answers. ") +
                                            len("Incorrect answers. "):
                                            div.text.index(" are the correct answers.")]
                except ValueError:
                    correct_answer = div.text[div.text.index("Incorrect answers. ") +
                                            len("Incorrect answers. "):
                                            div.text.index(" is the correct answer.")]

                correct_answer = correct_answer.replace(' ', '')

                correct_answer = correct_answer.split(',')

                for item in correct_answer:
                    result_to_return[title].append(dict_letter_answer[item])
            elif 'Correct answers' in div.text:
                result_to_return[title].append(dict_letter_answer['A'])
                

        return result_to_return

    def click_associated_answer(self, answer_input_id):
        # On récupère toutes les options
        options = self.browser.find_element(By.XPATH, "//ul[@class='Matching---ul---bIrQZ']")

        for li in options.find_elements(By.XPATH, "//li[@class='Matching---option---1L906']"):
            content = li.text

            letter = content[:content.index(':')]

            answer = content[content.index(':') + 1:]

            for key in answer_input_id:
                if answer in answer_input_id[key]:
                    # Trouve la bonne div et la bonne lettre et clique dessus
                    self.browser.find_element(By.XPATH, "//span[text()='"
                                                       + key + "']/parent::legend/following-sibling::div"
                                                               "//span[text()='" + letter + "']").click()

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)
        
    def find_associated_answer_radio(self):
        result_to_return = {}

        self.browser.find_element(By.XPATH, "//div[@class='RadioButton---label---1dtPw RadioButton---spaced---aeCFF']").click()

        sleep(1)

        # On valide la réponse
        self.browser.find_element(By.XPATH, "//div[@class='Question---verifyButton---KIKC0']").click()

        sleep(2)

        # On récupère toutes les options
        options = self.browser.find_element(By.XPATH, "//ul[@class='Matching---ul---bIrQZ']")

        dict_letter_answer = {}

        for li in options.find_elements(By.XPATH, "//li[@class='Matching---option---1L906']"):
            content = li.text

            letter = content[:content.index(':')]

            answer = content[content.index(':') + 1:]

            dict_letter_answer[letter] = answer

        matching_choices = self.browser.find_elements(By.XPATH, "//fieldset")

        for div in matching_choices:
            title = div.text[:div.text.index('\n')]

            result_to_return[title] = []

            try:
                correct_answer = div.text[div.text.index("Incorrect answer. ") +
                                        len("Incorrect answer. "):
                                        div.text.index(" is the correct answer.")]
                correct_answer = correct_answer.replace(' ', '')
            except ValueError:
                #Bonne réponse donc c'est le premier radio bouton A
                correct_answer = 'A'
            result_to_return[title].append(dict_letter_answer[correct_answer])

        return result_to_return

    def test_is_passed(self):
        try:
            score = self.browser.find_element(By.CLASS_NAME, "Assessment---scoreNumber---HtCXE").text
            if score == "100%":
                print(score)
                return True
            return False
        except:
            return False
        
