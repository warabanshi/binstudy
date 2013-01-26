#include <unistd.h>

void main() {
    const char msg[] = "AB";
    //write(STDOUT_FILENO, &a, 1);
    write(1, &msg, 2);
    return ;
}
