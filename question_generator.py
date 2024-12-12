import PyPDF2
import spacy
import random
import os
import nltk

nltk.download('wordnet', quiet=True)
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

class PDFQuestionGenerator:
    def __init__(self, pdf_path):
        """
        Initialize the question generator with a PDF file.
        
        :param pdf_path: Path to the PDF file
        """
        self.pdf_path = pdf_path
        self.text = self._extract_text()
        
        # Load spaCy model for named entity recognition and dependency parsing
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Downloading spaCy English model...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load('en_core_web_sm')

    def _extract_text(self):
        """
        Extract text from the PDF file.
        
        :return: Extracted text as a string
        """
        text = ""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def generate_wh_questions(self, num_questions=5):
        """
        Generate WH-questions (Who, What, Where, When, Why) from the text.
        
        :param num_questions: Number of questions to generate
        :return: List of generated questions
        """
        # Process the text with spaCy
        doc = self.nlp(self.text)
        
        # Extract potential question sources
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        sentences = list(doc.sents)
        
        questions = []
        while len(questions) < num_questions and sentences:
            # Randomly select a sentence
            sentence = random.choice(sentences)
            sentences.remove(sentence)
            
            # Try to generate different types of WH questions
            question_types = [
                self._generate_who_question,
                self._generate_what_question,
                self._generate_where_question,
                self._generate_when_question
            ]
            
            for question_type in question_types:
                q = question_type(sentence, entities)
                if q and q not in questions:
                    questions.append(q)
                    break
            
            if len(questions) >= num_questions:
                break
        
        return questions

    def _generate_who_question(self, sentence, entities):
        """
        Generate a 'Who' question based on the sentence and entities.
        """
        person_entities = [ent for ent in entities if ent[1] == 'PERSON']
        
        if person_entities:
            entity = random.choice(person_entities)[0]
            question = f"Who {sentence.text.replace(entity, '...')}"
            return question
        return None

    def _generate_what_question(self, sentence, entities):
        """
        Generate a 'What' question based on the sentence.
        """
        nouns = [chunk.text for chunk in sentence.noun_chunks]
        
        if nouns:
            noun = random.choice(nouns)
            question = f"What {sentence.text.replace(noun, '...')}"
            return question
        return None

    def _generate_where_question(self, sentence, entities):
        """
        Generate a 'Where' question based on the sentence and entities.
        """
        location_entities = [ent for ent in entities if ent[1] in ['GPE', 'LOC']]
        
        if location_entities:
            entity = random.choice(location_entities)[0]
            question = f"Where {sentence.text.replace(entity, '...')}"
            return question
        return None

    def _generate_when_question(self, sentence, entities):
        """
        Generate a 'When' question based on the sentence and entities.
        """
        time_entities = [ent for ent in entities if ent[1] in ['DATE', 'TIME']]
        
        if time_entities:
            entity = random.choice(time_entities)[0]
            question = f"When {sentence.text.replace(entity, '...')}"
            return question
        return None