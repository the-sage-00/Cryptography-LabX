#include <iostream>
#include <string>
#include <cctype>
using namespace std;

string encrypt(string text, int key) {
    string result = "";

    for (char ch : text) {
        if (isalpha(ch)) {
            char base = isupper(ch) ? 'A' : 'a';
            result += char((ch - base + key) % 26 + base);
        } else {
            result += ch;
        }
    }

    return result;
}

string decrypt(string text, int key) {
    return encrypt(text, (26 - key) % 26);
}

int main() {
    string plaintext;
    int key;

    cout << "Enter plaintext: ";
    getline(cin, plaintext);

    cout << "Enter key: ";
    cin >> key;

    string ciphertext = encrypt(plaintext, key);

    cout << "\nEncrypted text: " << ciphertext << endl;
    cout << "Decrypted text: " << decrypt(ciphertext, key) << endl;

    return 0;
}