#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define Npontos 100000      //Numero de pontos do arquivo de dados
#define Npontos_bc 6        //Numero de pontos gerado no box-countung  
#define Lx 1                //Comprimento x da area analisada
#define Ly 1                //Comprimento y da area analisada  
#define Nfile 1000

int varredura(float x, float y, float l, float valoresx[Npontos], float valoresy[Npontos]);
void box_counting(float valoresx[Npontos], float valoresy[Npontos], float bc_logl[Npontos_bc], float bc_logn[Npontos_bc], int idx_file);


int main()
{

    int i, k;
    float parabolax[Npontos], parabolay[Npontos], x, y, l;
    float valoresx[Npontos], valoresy[Npontos], bc_logl[Npontos_bc], bc_logn[Npontos_bc];
    double a=0;
    double b=0;
    int bufferLength = 1024;
    char buffer[bufferLength];
    char filename[100], old_filename[100], new_filename[100];

    for (i = k; k < Nfile; k++)
    {

        
        sprintf(filename, "file_sa_1700/data_%d.dat", k);

        FILE *fp = fopen(filename, "r");
        if (!fp)
        {
            printf("Cant open file\n");
            return -1;
        }

        i = 0;
        while(fgets(buffer, bufferLength, fp))
        {
            //printf("%s\n", buffer);   
            if (2==sscanf(buffer, "%lf %lf", &a,&b))
            {
                //printf("a: %f   b: %f\n", a,b);
                valoresx[i] = a;
                valoresy[i] = b;
                i = i+1;

            }
        }

        fclose(fp);


        for(i = 0; i < Npontos; i++)
        {
            //printf("i = %d   valorx = %f   valory = %f\n",i,valoresx[i],valoresy[i]);
            x = (i*1.0/Npontos);
            y = sin(x);
            parabolax[i] = x;
            parabolay[i] = y;
        }
        
    
        time_t begin = time(NULL);
        box_counting(valoresx, valoresy, bc_logl, bc_logn, k);
        time_t end = time(NULL);
    
        printf("Time = %ld s = %lf min\n", (end - begin),(end - begin)/60.0);

        sprintf(old_filename, "DADOS_BC_%d.dat", k);

        sprintf(new_filename, "DADOS_BC_saud_1700rpm/DADOS_BC_%d.dat", k);



        if (rename(old_filename, new_filename) == 0) {
            printf("Arquivo %d movido com sucesso!\n\n",k);
        } else {
            perror("Erro ao mover arquivo");
        }
    

    }

    return 0;
}



void box_counting(float valoresx[Npontos], float valoresy[Npontos], float bc_logl[Npontos_bc], float bc_logn[Npontos_bc], int idx_file)
{
    int i, j, k, nx, ny, ocupacao, contagem;
    float l, x, y;
    char filename[100];

    sprintf(filename, "DADOS_BC_%d.dat", idx_file);
    FILE *fd = fopen(filename,"w");

    l = 1.0;
    while(l > 0.0015625)
    {
        nx = (int)(Lx/l);
        ny = (int)(Ly/l);
        
        contagem=0;
        for(i = 0; i < nx; i++)
        {
            for(j = 0; j < ny; j++)
            {
                x = j*((float)Lx/nx);
                y = i*((float)Lx/ny);
                
                ocupacao = varredura(x, y, l, valoresx, valoresy);
                if(ocupacao == 1)
                {
                    contagem++;
                }
            }
        }

        printf("l = %f   contagem = %d\n",l,contagem);
        
        
        fprintf(fd,"%f %f\n", log10(1/l),log10(contagem));
        
        
        l=l/2.0;
    }

    fclose(fd);
}


int varredura(float x, float y, float l, float valoresx[Npontos], float valoresy[Npontos])
{
    int i;
    float valx, valy;

    for(i = 0; i < Npontos; i++)
    {
        valx = valoresx[i];
        valy = valoresy[i];

        if(valx > x && valx < x+l)  
        {
            if(valy > y && valy < y+l)
            {
                //printf("deu certo\n");
                return 1;
            }   
        }

    }

    return 0;
}