# Org to IPYNB

## Requirements
- jupyter notebook

```bash
pip3 install jupyter jupyter-c-kernel jupyterlab notebook
``` 
puis 
```bash
install_c_kernel --user
```
- gcc
    - OpenMP

Vous pouvez tester si tout marche à l'aide de cette commande et de ce fichier :
```bash
gcc -fopenmp code_block.c -o codeblock
./code_block
```
```c
// OpenMP header
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
 
int main(int argc, char* argv[])
{
    int nthreads, tid;
 
    // Begin of parallel region
    #pragma omp parallel private(nthreads, tid)
    {
        // Getting thread number
        tid = omp_get_thread_num();
        printf("Welcome to GFG from thread = %d\n",
               tid);
 
        if (tid == 0) {
 
            // Only master thread does this
            nthreads = omp_get_num_threads();
            printf("Number of threads = %d\n",
                   nthreads);
        }
    }
}
```

## Principe

On prend un .org que l'on convertit en html à l'aide de `pandoc <filename>.org -o <filename>.html`.
Ensuite on parse ce rendu intermédiaire pour en extraire les bouts de codes et générer un json exploitable IPYNB.

## Utilisation
```text
Usage : jupytorg src=input_file_path (optional type=code_block_language dest=output_file_path)
    input_file_path : the path to input the file
    code_block_language : le language des blocks de code (default is C)
    output_file_path : the path to output the file (default is output_file.ipynb)
```
Exemple avec un fichier `newcourse.org` :
```bash
jupytorg src=~/Documents/2A/OpenMP/newcourse.org dest=~/Documents/2A/OpenMP/newcourse.ipynb
```
Il va lire le fichier `.org` dans le dossier spécifié et va déposer dans ce même dossier le jupyter notebook coonverti. Il ne reste plus qu'à l'ouvrir avec VSCode.
