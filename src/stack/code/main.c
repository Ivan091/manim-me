int foo(int a, int &b) {
    int c = 10;
    {
        int d = 5;
        b = d + c;
    }
    return a;
}

int main() {
    int x = 4;
    int y = 7;
    int v = foo(x, y);
    printf("%d", v);
    return 0;
}