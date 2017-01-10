import os, re, sys
import shutil
import logging

PIC_EXTENSIONS = ['.jpg', '.png', '.gif']
VIDEO_EXTENSIONS = ['.avi', '.mov', '.mp4', '.wmv', '.mpg']


class VideoPictureSeparator(object):
        
    def __init__(self, options):
        
        self.options = options
        self.paths = {}
        
        #Setting up logger.
        self.log = logging.getLogger('VideoPictureSeparator')
        self.log.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("VideoPictureSeparator.log", mode='w', encoding='UTF-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.log.addHandler(fileHandler)
        self.log.info("Initialized VideoPictureSeparator")
    
    def run(self):
        picCount = 0
        videoCount = 0
        for root, dirs, files in os.walk(self.options.source_dir):
            for f in files:
                path, ext = os.path.splitext(f)
                if ext.lower() in PIC_EXTENSIONS:
                    picCount += 1
                elif  ext.lower() in VIDEO_EXTENSIONS:
                    targetDir = root.replace(self.options.source_dir, self.options.target_dir_vids)
                          
                    self.__copy_or_move(os.path.join(root, f), os.path.join(targetDir, f))
                    videoCount += 1
                else:
                    print("Unknown extension {}", os.path.join(root, f))
                    
        print("Pictures {}", picCount)
        print("Videos {}", videoCount)
        
    def __copy_or_move(self, source, target):
        """
        Internal function to perform copy or move based on the command line
        arguments. Supports also dry-run option which only writes information
        to the log file.
        """
        
        if self.options.dry_run:
            self.log.info('Dry-run copy or move {} -> {}'.format(source, target))
        else:
            
            if not os.path.isdir(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            
            if self.options.copy:
                shutil.copy2(source, target)
            else:
                shutil.move(source, target)  


def main():
    import argparse

    # setup command line parsing
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Organizes separates pictures and videos to two folders.')
    parser.add_argument('source_dir', type=str, help='source directory')
    parser.add_argument('target_dir_vids', type=str, help='target directory for videos')
    parser.add_argument('-c', '--copy', action='store_true', help='copy files instead of move')
    parser.add_argument('--dry-run', action='store_true', help='Performs only analysis, not doing actual moving or copying')
    # parse command line arguments
    options = parser.parse_args()


    videoPicSeparator = VideoPictureSeparator(options)
    videoPicSeparator.run();
    
    
if __name__ == '__main__':
    main()