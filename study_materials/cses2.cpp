#include<iostream>
using namespace std;

int main(){
    long long n;
    cin >> n;

    // Since the array indices are 0-based, we should declare the array with size n+1
    long long arr[n + 1];

    // Input the array elements
    for(int i = 2; i <= n; i++){
        cin >> arr[i];
    }

    long long sum = 0;
    for(int i = 2; i <= n; i++){ // Corrected the loop range to include all elements of the array
        sum = sum + arr[i];
    }

    // The formula to calculate the sum of first n natural numbers is (n * (n + 1)) / 2
    cout << ((n * (n + 1)) / 2) - sum; // Corrected the expression for finding the missing number
    return 0;
}

