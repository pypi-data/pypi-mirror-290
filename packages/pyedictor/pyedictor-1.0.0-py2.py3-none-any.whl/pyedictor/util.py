import urllib
from urllib.request import urlopen
import tempfile
import lingpy


def fetch(
    dataset,
    remote_dbase=None,
    concepts=None,
    languages=None,
    columns=None,
    to_lingpy=None,
    transform=None,
    base_url="http://lingulist.de/edictor",
):
    url = base_url + "/triples/get_data.py?file=" + dataset
    if not remote_dbase:
        url += "&remote_dbase=" + dataset + ".sqlite3"
    else:
        url += "&remote_dbase=" + remote_dbase
    if concepts:
        url += "&concepts=" + "|".join([urllib.parse.quote(c) for c in concepts])
    if languages:
        url += "&doculects=" + "|".join([urllib.parse.quote(c) for c in languages])
    if columns:
        url += "&columns=" + "|".join(columns)

    data = urlopen(url).read()
    if to_lingpy:
        with tempfile.NamedTemporaryFile() as tf:
            tf.write(data)
            tf.flush()
            return transform(tf.name) if transform else lingpy.Wordlist(tf.name)
    return data.decode("utf-8")


def iter_etymdict(wordlist, ref, *values):
    for cogid, idxs_ in wordlist.get_etymdict(ref).items():
        idxs = []
        for idx in idxs_:
            if idx:
                idxs += idx
        if not values:
            yield cogid, idxs
        yield cogid, [idxs] + [[wordlist[idx, val] for idx in idxs] for val in values]
