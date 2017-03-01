#placehlder file - scruipt supposed to make bash scripts for kraken


   sh = open(output_prefix + sh_file, 'w')
   sh.write('#!/bin/sh\n')


      sh.write('\n')
         sh.write(
            '/pbs_home/hjaajensen/progs/gitDalton/build_apsg/dalton -dal _ccsd.dal -mol '+tname+'\n'
            )


   sh.close();