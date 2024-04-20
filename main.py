import argparse
from Workers import CrawlSpider_site, CrawlerProcess
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--site_name', default='google', type=str)
    args.add_argument('--out_dir', default=None, type=str)
    cmd_args = args.parse_args()
    assert cmd_args.site_name is not None, "Please specify the name of the online newspaper"
    if cmd_args.out_dir is None:
        cmd_args.out_dir = 'data/'
    # Set the output filename
    FILE_NAME = '{}/{}.jsonl'.format(cmd_args.out_dir, cmd_args.site_name)
    SETTINGS = {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                'FEED_FORMAT': 'jsonlines',
                'FEED_URI': FILE_NAME,
                'CONCURRENT_ITEMS': 1}
    process = CrawlerProcess(SETTINGS)
    process.crawl(CrawlSpider_site)
    process.start()
    print('Done')