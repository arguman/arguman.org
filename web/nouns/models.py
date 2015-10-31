from unidecode import unidecode

from django.db import models
from django.utils.encoding import smart_unicode
from django.template.defaultfilters import slugify

from nouns.utils import get_synsets, get_lemmas, from_lemma


class Noun(models.Model):
    text = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, blank=True)
    hypernyms = models.ManyToManyField('self', blank=True, null=True,
                                       related_name='hyponyms', 
                                       symmetrical=False)
    antonyms = models.ManyToManyField('self', blank=True, null=True,
                                       related_name='antonyms')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return smart_unicode(self.text).title()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.text))
        return super(Noun, self).save(*args, **kwargs)

    @classmethod
    def from_synset(cls, synset):
        lemmas = synset.lemma_names()
        text = lemmas[0]
        synonyms = lemmas[1:]
        noun, created = cls.objects.get_or_create(
            text=from_lemma(text),
            defaults={
                'is_active': False
            })
        for synonym in synonyms:
            noun.add_synonym(from_lemma(synonym))
        return noun

    def update_with_wordnet(self, update_antonyms=True):
        synsets = get_synsets(self.text)

        if not synsets:
            return

        for synset in synsets:
            path = synset.hypernym_paths()[0]
            parents = path[:-1]
            parent = self
            for hypernym in reversed(parents):
                noun = Noun.from_synset(hypernym)
                parent.hypernyms.add(noun)
                parent = noun

        for lemma in get_lemmas(self.text):
            if lemma != self.text:
                self.add_synonym(lemma)

        if not update_antonyms:
            return

        for synset in synsets:
            for lemma in synset.lemmas():
                for antonym in lemma.antonyms():
                    noun = Noun.from_synset(antonym.synset())
                    self.antonyms.add(noun)
                    noun.update_with_wordnet(update_antonyms=False)

    def add_synonym(self, text):
        synonym, created = self.synonyms.get_or_create(text=text)
        return synonym

    @models.permalink
    def get_absolute_url(self):
        return 'nouns_detail', [self.slug]


class Synonym(models.Model):
    noun = models.ForeignKey(Noun, related_name="synonyms")
    text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return smart_unicode(self.text)


class Pattern(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    def __unicode__(self):
        return smart_unicode(self.name)

