import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtMultimedia import QSound
import dict_ui
from functools import partial
from wiktionaryparser import WiktionaryParser

NO_RESULT = "[{'etymology': '', 'definitions': [], 'pronunciations': {'text': [], 'audio': []}}]"

def generate_result(ui):
    word = fetch_word(ui)
    result = parse_word(word)
    show_word(result, ui)

def fetch_word(ui):
    parser = WiktionaryParser()
    parser.set_default_language('hungarian')
    input = ui.lineEdit.text()
    word = parser.fetch(input)
    return word

def parse_word(word):
    if str(word) == NO_RESULT:
        definitions_output = "no_result"
        Etymology_output = "no_result"
        Pronunciation_output = "no_result"
        return definitions_output, Etymology_output, Pronunciation_output
    else:
        word = word[0]
        # Definition
        definitions_output = ""
        definitions = word["definitions"]
        for item in definitions:
            partOfSpeech = item["partOfSpeech"]
            text = item["text"]
            relatedWords = item["relatedWords"]
            examples = item["examples"]
            text_output = ""
            text_item_cnt = 1
            for text_item in text:
                if text_item_cnt == 1:
                    text_output = text_output + "<h2>"  + text_item + "</h2>"
                else:
                    text_output = text_output + "<h2>" + str(text_item_cnt-1) + ". " + text_item + "</h2>"
                text_item_cnt += 1
            definitions_output = definitions_output + "<h1>" + partOfSpeech + "</h1>" + text_output
            if relatedWords != []:
                relatedWords_output = ""
                for relatedWords_item in relatedWords:
                    relationshipType = relatedWords_item["relationshipType"]
                    word_output = ""
                    for single_word in relatedWords_item["words"]:
                        word_output = word_output + single_word + ","
                    word_output = word_output.rstrip(",")
                    relatedWords_output = relatedWords_output + "<h2>" + relationshipType + ": " + word_output + "</h2>" 
                definitions_output = definitions_output + relatedWords_output
            if examples != []:
                examples_output = ""
                for examples_item in examples:
                    examples_output = examples_output + "<h3>" + examples_item + "</h3>"
                definitions_output = definitions_output + "\n" + examples_output
        # Etymology
        Etymology_output = word["etymology"]
        # Pronunciation
        Pronunciation_output = word["pronunciations"]
        return definitions_output, Etymology_output, Pronunciation_output

def show_word(result, ui):
    if result[0] == "no result":
        show_text = "<h1>no result</h1>"
        ui.textBrowser.setHtml(show_text)
    else:
        definitions_output = result[0]
        Etymology_output = result[1]
        Pronunciation_output = result[2]
        ui.textBrowser.setHtml(definitions_output)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = dict_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.pushButton.clicked.connect(partial(generate_result, ui))
    sys.exit(app.exec_())