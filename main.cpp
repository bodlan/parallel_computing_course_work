#include <iostream>
#include <fstream>
#include <string>
int main(int argc,char *argv[]){

    std::string line;
    std::ifstream f("testfile.txt");
    if(f.is_open()){
        while (getline(f,line))
        {
            std::cout<<line<<std::endl;

        }
        
    }
    f.close();
    std::cout<<"Count of args: "<<argc<<std::endl;
    for(int i=0;i<argc; i++){
        std::cout<<argv[i]<<std::endl;
    }
    return 0;

}