from src import utils
from src.reader import Reader
from src.retrieval import Indexer, Searcher
from src import metrics
from src.argparse import parse_args
import lucene
import os
import sys

all_langs = ['en', 'de', 'es']

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        for k, v in vars(args).items():
            print("{0: <12}: {1}".format(k,v))
        sys.exit(0)
    # start java VM
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    if args.create:
        langs = [args.language]
        if args.language == 'all':
            langs = all_langs
        for lang in langs:
            if args.analyzer == None:
                analyzer = lang
            indexer = Indexer(
                index_path=args.index,
                data_path=args.index,
                lang=lang,
                dataset=args.dataset,
                analyzer=analyzer,
                ram_size=args.ram_size)
            indexer.createIndex()

    if args.query != None:
        #if not os.path.isfile(idxfile):
        #    raise Exception("Could not find indexfile: {}".format(idxfile))
        if args.analyzer == None or args.language == 'all':
            raise ValueError("To retrieve query you must specify analyzer and language")
        searcher = Searcher(
                index_path=args.index,
                lang=args.language,
                analyzer=args.analyzer,
                dataset=args.dataset)
        searcher.queryTest(args.query)

    if args.run == 'reader':
        reader = Reader()
        reader.run(
                lang=args.lang,
                analyzer=args.analyzer,
                dataset=args.dataset)
    if args.metric == 'dist':
        metrics.hits(
               dataset=args.dataset,
               langContext=args.language,
               langQuestion=args.language,
               distant=True,
               k=50)

    if args.metric == 'hit@k':
        metrics.hits(
               dataset=args.dataset,
               langContext=args.language,
               langQuestion=args.language,
               distant=False,
               k=50)

    if args.metric == 'qa_f1':
        metrics.qa_f1(
               dataset=args.dataset,
               eval_dataset=args.eval_dataset,
               langSearch=args.language,
               langQuestion=args.language,
               k=10)

    if args.metric == 'review':
        metrics.review(
               dataset=args.dataset,
               eval_dataset=args.eval_dataset,
               langContext=args.language,
               langQuestion=args.language,
               k=10)
