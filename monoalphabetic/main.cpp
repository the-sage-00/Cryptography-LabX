#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <cctype>

using namespace std;

string read_file(const string& filename)
{
    ifstream file(filename);

    if (!file)
    {
        cout << "Error opening " << filename << endl;
        return "";
    }

    string text;
    string line;

    while (getline(file, line))
    {
        text += line;
        text += '\n';
    }

    file.close();
    return text;
}

void write_file(const string& filename, const string& text)
{
    ofstream file(filename);

    if (!file)
    {
        cout << "Error creating " << filename << endl;
        return;
    }

    file << text;
    file.close();
}

string generate_key()
{
    return "QWERTYUIOPASDFGHJKLZXCVBNM";
}

string encrypt_text(const string& plaintext, const string& key)
{
    string ciphertext = "";

    for (char ch : plaintext)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            bool upper = isupper(static_cast<unsigned char>(ch));
            char upperChar = toupper(static_cast<unsigned char>(ch));
            int index = upperChar - 'A';
            char encrypted = key[index];

            if (!upper)
            {
                encrypted = tolower(
                    static_cast<unsigned char>(encrypted)
                );
            }

            ciphertext += encrypted;
        }
        else
        {
            ciphertext += ch;
        }
    }

    return ciphertext;
}

void frequency_analysis(const string& ciphertext)
{
    int frequency[26] = {0};
    int totalLetters = 0;

    for (char ch : ciphertext)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            char c = toupper(static_cast<unsigned char>(ch));
            frequency[c - 'A']++;
            totalLetters++;
        }
    }

    vector<pair<char, int>> freq;

    for (int i = 0; i < 26; i++)
    {
        freq.push_back({'A' + i, frequency[i]});
    }

    sort(freq.begin(), freq.end(),
         [](const pair<char, int>& a,
            const pair<char, int>& b)
         {
             return a.second > b.second;
         });

    cout << "\n========================================\n";
    cout << "LETTER FREQUENCY ANALYSIS\n";
    cout << "========================================\n";

    cout << "Letter\tCount\tPercentage\n";

    for (auto item : freq)
    {
        double percentage = 0.0;

        if (totalLetters > 0)
        {
            percentage =
                (item.second * 100.0) / totalLetters;
        }

        cout << item.first << "\t"
             << item.second << "\t"
             << percentage << "%\n";
    }

    cout << "\nMost frequent ciphertext letters:\n";

    for (int i = 0; i < 5; i++)
    {
        cout << freq[i].first
             << " (" << freq[i].second << ") ";

        if (i != 4)
            cout << "-> ";
    }

    cout << "\n";
}

string uppercase_word(string word)
{
    for (char& c : word)
    {
        c = toupper(static_cast<unsigned char>(c));
    }

    return word;
}

void word_frequency_analysis(const string& ciphertext)
{
    map<string, int> wordCount;
    string word = "";

    for (size_t i = 0; i <= ciphertext.length(); i++)
    {
        char ch;

        if (i < ciphertext.length())
            ch = ciphertext[i];
        else
            ch = ' ';

        if (isalpha(static_cast<unsigned char>(ch)))
        {
            word += toupper(
                static_cast<unsigned char>(ch)
            );
        }
        else
        {
            if (!word.empty())
            {
                wordCount[word]++;
                word = "";
            }
        }
    }

    vector<pair<string, int>> words(
        wordCount.begin(),
        wordCount.end()
    );

    sort(words.begin(), words.end(),
         [](const pair<string, int>& a,
            const pair<string, int>& b)
         {
             return a.second > b.second;
         });

    cout << "\n========================================\n";
    cout << "WORD FREQUENCY ANALYSIS\n";
    cout << "========================================\n";

    cout << "Word\tFrequency\n";

    int shown = 0;

    for (auto item : words)
    {
        cout << item.first
             << "\t"
             << item.second
             << "\n";

        shown++;

        if (shown == 20)
            break;
    }

    cout << "\nOne-letter words:\n";

    for (auto item : words)
    {
        if (item.first.length() == 1)
        {
            cout << item.first
                 << " -> "
                 << item.second
                 << "\n";
        }
    }

    cout << "\nTwo-letter words:\n";

    for (auto item : words)
    {
        if (item.first.length() == 2)
        {
            cout << item.first
                 << " -> "
                 << item.second
                 << "\n";
        }
    }

    cout << "\nThree-letter words:\n";

    for (auto item : words)
    {
        if (item.first.length() == 3)
        {
            cout << item.first
                 << " -> "
                 << item.second
                 << "\n";
        }
    }
}

string get_pattern(const string& word)
{
    map<char, int> seen;
    int nextNumber = 0;
    string pattern = "";

    for (char c : word)
    {
        if (seen.find(c) == seen.end())
        {
            seen[c] = nextNumber;
            nextNumber++;
        }

        pattern += to_string(seen[c]);
        pattern += " ";
    }

    return pattern;
}

void pattern_analysis(const string& ciphertext)
{
    cout << "\n========================================\n";
    cout << "PATTERN ANALYSIS\n";
    cout << "========================================\n";

    string word = "";

    for (size_t i = 0; i <= ciphertext.length(); i++)
    {
        char ch;

        if (i < ciphertext.length())
            ch = ciphertext[i];
        else
            ch = ' ';

        if (isalpha(static_cast<unsigned char>(ch)))
        {
            word += toupper(
                static_cast<unsigned char>(ch)
            );
        }
        else
        {
            if (!word.empty())
            {
                if (word.length() >= 3)
                {
                    cout << word
                         << "\tPattern: "
                         << get_pattern(word)
                         << "\n";
                }

                word = "";
            }
        }
    }
}

string apply_substitution(
    const string& ciphertext,
    const map<char, char>& substitution)
{
    string result = "";

    for (char ch : ciphertext)
    {
        if (isalpha(static_cast<unsigned char>(ch)))
        {
            bool upper =
                isupper(static_cast<unsigned char>(ch));

            char c =
                toupper(static_cast<unsigned char>(ch));

            if (substitution.find(c) != substitution.end())
            {
                char replacement =
                    substitution.at(c);

                if (!upper)
                {
                    replacement =
                        tolower(
                            static_cast<unsigned char>(
                                replacement
                            )
                        );
                }

                result += replacement;
            }
            else
            {
                result += '_';
            }
        }
        else
        {
            result += ch;
        }
    }

    return result;
}

void display_partial_plaintext(
    const string& ciphertext,
    const map<char, char>& substitution)
{
    string partial =
        apply_substitution(
            ciphertext,
            substitution
        );

    cout << "\n========================================\n";
    cout << "PARTIAL PLAINTEXT\n";
    cout << "========================================\n";

    if (partial.length() > 1500)
    {
        cout << partial.substr(0, 1500)
             << "\n...\n";
    }
    else
    {
        cout << partial << "\n";
    }
}

bool verify_solution(
    const string& recoveredPlaintext,
    const string& ciphertext,
    const string& key)
{
    string generated =
        encrypt_text(
            recoveredPlaintext,
            key
        );

    return generated == ciphertext;
}

map<char, char> create_inverse_key(
    const string& key)
{
    map<char, char> inverse;

    for (int i = 0; i < 26; i++)
    {
        char plain = 'A' + i;
        char cipher = key[i];

        inverse[cipher] = plain;
    }

    return inverse;
}

void display_key(const string& key)
{
    cout << "\n========================================\n";
    cout << "SUBSTITUTION KEY\n";
    cout << "========================================\n";

    cout << "Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";
    cout << "Cipher: " << key << "\n";

    cout << "\nIndividual mappings:\n";

    for (int i = 0; i < 26; i++)
    {
        cout << char('A' + i)
             << " -> "
             << key[i]
             << "\n";
    }
}

int main()
{
    cout << "========================================\n";
    cout << "MONOALPHABETIC SUBSTITUTION CIPHER\n";
    cout << "GROUP 10\n";
    cout << "========================================\n";

    string plaintext =
        read_file("plaintext.txt");

    if (plaintext.empty())
    {
        cout << "Plaintext file is empty.\n";
        return 1;
    }

    cout << "\nPlaintext loaded successfully.\n";

    string key =
        generate_key();

    display_key(key);

    string ciphertext =
        encrypt_text(
            plaintext,
            key
        );

    write_file(
        "ciphertext.txt",
        ciphertext
    );

    cout << "\nCiphertext generated successfully.\n";

    frequency_analysis(
        ciphertext
    );

    word_frequency_analysis(
        ciphertext
    );

    pattern_analysis(
        ciphertext
    );

    map<char, char> recoveredKey;

    display_partial_plaintext(
        ciphertext,
        recoveredKey
    );

    map<char, char> inverse =
        create_inverse_key(key);

    string recoveredPlaintext =
        apply_substitution(
            ciphertext,
            inverse
        );

    write_file(
        "recovered.txt",
        recoveredPlaintext
    );

    cout << "\nRecovered plaintext generated.\n";

    bool verified =
        verify_solution(
            recoveredPlaintext,
            ciphertext,
            key
        );

    cout << "\n========================================\n";
    cout << "VERIFICATION\n";
    cout << "========================================\n";

    if (verified)
    {
        cout << "SUCCESS: Re-encryption matches ciphertext.\n";
    }
    else
    {
        cout << "FAILED: Re-encryption does not match ciphertext.\n";
    }

    return 0;
}
