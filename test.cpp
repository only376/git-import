#include<stdio.h>

int main()
{ 
    int count=0;
    int i;
    int x;
    int b[10000]; 
    scanf("%d",&x);
    while(x!=0){
            b[count]=x;
            count++;
            scanf("%d",&x);
        }
    int c[count];
    for(i=0;i<count;i++){
        c[i]=b[count-i-1];
    }
    for(i=0;i<count;i++){
        printf("%d",c[i]);
        if(i<count-1){
            printf(" ");
        }
    }    
    return 0;
}
