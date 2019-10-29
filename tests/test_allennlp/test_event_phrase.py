import pytest

from sheenroo_algs.allennlp.event_phrase import get_svo_detail_pairs_sent, PairFlags


@pytest.mark.parametrize('sent, pairs', [
    ('I don\'t love you', {('I', 'love', 'you', PairFlags(negative=True))}),
    ('He is trying to seduce her and she doesn\'t want it.', {('He', 'trying', None, PairFlags()), ('He', 'seduce', 'her', PairFlags()), ('she', 'want', 'it', PairFlags(negative=True))}),
    ('She realized what she said a few seconds later and apologized profusely saying that is not what she meant.',
     {('She', 'realized', None, PairFlags()), ('she', 'said', 'what', PairFlags()), ('She', 'apologized', None, PairFlags()), ('that', 'is', None, PairFlags(negative=True)), ('she', 'meant', 'what', PairFlags()),
      ('She', 'saying', None, PairFlags())}),
    ('He started screaming that bread won\'t pay for beer and weed and yelled at me to go away and bring money next time.',
     {('He', 'screaming', None, PairFlags()), ('He', 'started', None, PairFlags()), ('bread', 'pay for', None, PairFlags(negative=True))}),
    ('One week later he sells the truck and never pays me for the motor.', {('he', 'sells', 'the truck', PairFlags()), ('he', 'pays for', 'me', PairFlags(negative=True))}),
])
def test_get_svo_detail_pairs_sent_neg(sent, pairs):
    output_pairs = get_svo_detail_pairs_sent(sent)
    assert output_pairs == pairs, f'A test data\'s pairs did not match the expected output (Sent: "{sent}", Expected: "{pairs}", Actual: "{output_pairs}")'


@pytest.mark.parametrize('sent, pairs', [
    ('Based on the pictures I dug up, my frog is a bitch.', {('I', 'dug up', None, PairFlags())}),
    ('I love you', {('I', 'love', 'you', PairFlags())}),
    ('I love you and I climbed a tree', {('I', 'love', 'you', PairFlags()), ('I', 'climbed', 'a tree', PairFlags())}),
    ('I love you and I climbed up a tree', {('I', 'love', 'you', PairFlags()), ('I', 'climbed up', 'a tree', PairFlags())}),
    ('I have loved you and her', {('I', 'loved', 'you and her', PairFlags())}),
    ('Your mum and I love you', {('Your mum and I', 'love', 'you', PairFlags())}),
    ('He is trying to seduce her.', {('He', 'trying', None, PairFlags()), ('He', 'seduce', 'her', PairFlags())}),
    ('He is trying to seduce her and hug her.', {('He', 'trying', None, PairFlags()), ('He', 'seduce', 'her', PairFlags()), ('He', 'hug', 'her', PairFlags())}),
    ('He is trying to seduce her, kiss her and hug her.', {('He', 'trying', None, PairFlags()), ('He', 'seduce', 'her', PairFlags()), ('He', 'kiss', 'her', PairFlags()), ('He', 'hug', 'her', PairFlags())}),
    ('I am learning to dance.', {('I', 'learning', None, PairFlags()), ('I', 'dance', None, PairFlags())}),
    ('I am learning to play you.', {('I', 'learning', None, PairFlags()), ('I', 'play', 'you', PairFlags())}),
    ('I hit you and punched her', {('I', 'hit', 'you', PairFlags()), ('I', 'punched', 'her', PairFlags())}),
    ('I hit you, punched her and kicked him', {('I', 'hit', 'you', PairFlags()), ('I', 'punched', 'her', PairFlags()), ('I', 'kicked', 'him', PairFlags())}),
    ('She got home safe', {('She', 'got', None, PairFlags())}),
    ('I spent time looking after her.', {('I', 'spent', 'time', PairFlags()), ('I', 'looking after', None, PairFlags())}),
    ('I spent that entire evening looking after her, my friends all walked off, and made sure she got home safe.',
     {('I', 'spent', None, PairFlags()), ('I', 'looking after', None, PairFlags()), ('my friends all', 'walked off', None, PairFlags()), ('I', 'made', None, PairFlags())}),
    ('Saved a girl on an escalator when she got her heel stuck and fell backwards.',
     {('she', 'got', None, PairFlags()), ('she', 'fell', None, PairFlags()), ('her heel', 'stuck', None, PairFlags())}),
    ('If you\'re telling me you are, and refuse to be wrong, then I will go out in the back yard, get a large stick, shove it up your asshole, and you can tell me how much you enjoy it.',
     {('I', 'go out', None, PairFlags()), ('you', 'are', None, PairFlags()), ('you', 'refuse', None, PairFlags()), ('I', 'get', 'a large stick', PairFlags()),
      ('I', 'shove up', 'it', PairFlags()), ('you', 'tell', 'me', PairFlags()), ('you', 'telling', 'me', PairFlags()), ('you', 'enjoy', 'it', PairFlags())}),
])
def test_get_svo_detail_pairs_sent(sent, pairs):
    output_pairs = get_svo_detail_pairs_sent(sent)
    assert output_pairs == pairs, f'A test data\'s pairs did not match the expected output (Sent: "{sent}", Expected: "{pairs}", Actual: "{output_pairs}")'


@pytest.mark.parametrize('sent, pairs', [
    ('She realized what she said a few seconds later and apologized profusely saying that is not what she meant.',
     {('She', 'realized', None, PairFlags()), ('she', 'said', 'what', PairFlags()), ('She', 'apologized', None, PairFlags()), ('She', 'saying', None, PairFlags()), ('that', 'is', None, PairFlags(negative=True)), ('she', 'meant', 'what', PairFlags())}),
    ('I drank too much and found out to be torn apart by my mom',
     {('I', 'drank', 'too much', PairFlags()), ('I', 'torn by', None, PairFlags(passive=True)), ('I', 'found out', None, PairFlags())}),
])
def test_get_svo_detail_pairs_sent_conj_xcomp(sent, pairs):
    output_pairs = get_svo_detail_pairs_sent(sent)
    assert output_pairs == pairs, f'A test data\'s pairs did not match the expected output (Sent: "{sent}", Expected: "{pairs}", Actual: "{output_pairs}")'


@pytest.mark.parametrize('sent, pairs', [
    ('I was kicked', {('I', 'kicked', None, PairFlags(passive=True))}),
    ('I\'m freaked out just telling this.', {('I', 'telling', 'this', PairFlags()), ('I', 'freaked out', None, PairFlags(passive=True))}),
    ('I need to be beaten',
     {('I', 'need', None, PairFlags()), ('I', 'beaten', None, PairFlags(passive=True))}),
    ('My mum and I quickly left after that, but as a 5 year old, all I wanted to do was be kind, like I\'d been taught.',
     {('My mum and I', 'left after', None, PairFlags()), ('I', 'wanted', None, PairFlags()), ('I', 'do', None, PairFlags()), ('I', 'taught', None, PairFlags(passive=True))}),
])
def test_get_svo_detail_pairs_sent_passive(sent, pairs):
    output_pairs = get_svo_detail_pairs_sent(sent)
    assert output_pairs == pairs, f'A test data\'s pairs did not match the expected output (Sent: "{sent}", Expected: "{pairs}", Actual: "{output_pairs}")'


@pytest.mark.parametrize('sent, pairs', [
    ('The black professor standing right next to me punched my face', {('The professor', 'punched', 'my face', PairFlags())}),
    ('I kid you not there was a black midget with no arms standing about 5 feet in front of me.', {('I', 'kid', 'you', PairFlags()), ('a midget', 'was', None, PairFlags(negative=True))}),
    ('There is a woman standing next to me when a huge piece of dirt comes flying straight at her face.',
     {('a piece', 'comes', None, PairFlags()), ('a piece', 'flying at', None, PairFlags()), ('a woman', 'is', None, PairFlags())}),
])
def test_get_svo_detail_pairs_sent_nsubj(sent, pairs):
    output_pairs = get_svo_detail_pairs_sent(sent)
    assert output_pairs == pairs, f'A test data\'s pairs did not match the expected output (Sent: "{sent}", Expected: "{pairs}", Actual: "{output_pairs}")'


# @pytest.mark.parametrize('sent, pairs', [
#     ('My mom kicked and punched me with her high heels', {('My mom', 'kicked', 'me', PairFlags()), ('My mom', 'punched', 'me', PairFlags())}),
# ])
# def test_get_svo_detail_pairs_sent_multiple_dobj(sent, pairs):
#     output_pairs = get_svo_detail_pairs_sent(sent)
#     assert output_pairs == pairs, f'A test data\'s pairs did not match the expected output (Sent: "{sent}", Expected: "{pairs}", Actual: "{output_pairs}")'

# Problems:
# == Missing direct object, maybe looking for direct object from the parent
# The security sees me with a chunk of dirt in my hand and instantly grab and pull me out of the crowd.

# == No nsubj sentences
# Found a cell phone in the middle of the street.

# indirect object
# I give you $20

# passive

