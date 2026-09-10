#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cmath>

using namespace std;


string clean_ciphertext(string text)
{
    string result;

    for (char c : text)
    {
        if (isalpha(c))
            result += toupper(c);
    }

    return result;
}


vector<string> find_repeated_patterns(string text)
{
    vector<string> patterns;

    for (int i = 0; i <= (int)text.length() - 3; i++)
    {
        string pattern = text.substr(i, 3);

        bool found = false;

        for (string p : patterns)
        {
            if (p == pattern)
            {
                found = true;
                break;
            }
        }

        if (!found)
        {
            for (int j = i + 3; j <= (int)text.length() - 3; j++)
            {
                if (text.substr(j, 3) == pattern)
                {
                    patterns.push_back(pattern);
                    break;
                }
            }
        }
    }

    return patterns;
}


vector<int> calculate_distances(string text, string pattern)
{
    vector<int> positions;

    for (int i = 0; i <= (int)text.length() - 3; i++)
    {
        if (text.substr(i, 3) == pattern)
            positions.push_back(i);
    }

    vector<int> distances;

    for (int i = 0; i < (int)positions.size(); i++)
    {
        for (int j = i + 1; j < (int)positions.size(); j++)
        {
            distances.push_back(positions[j] - positions[i]);
        }
    }

    return distances;
}


vector<int> find_factors(int distance)
{
    vector<int> factors;

    for (int i = 2; i <= 20; i++)
    {
        if (distance % i == 0)
            factors.push_back(i);
    }

    return factors;
}


int kasiski_analysis(string text)
{
    vector<string> patterns = find_repeated_patterns(text);
    map<int, int> factor_count;

    cout << "\nRepeated patterns and distances:\n";

    for (string pattern : patterns)
    {
        vector<int> distances = calculate_distances(text, pattern);

        cout << pattern << " : ";

        for (int d : distances)
        {
            cout << d << " ";

            vector<int> factors = find_factors(d);

            for (int f : factors)
                factor_count[f]++;
        }

        cout << endl;
    }

    int best_length = 1;
    int best_count = 0;

    for (auto x : factor_count)
    {
        if (x.second > best_count)
        {
            best_count = x.second;
            best_length = x.first;
        }
    }

    return best_length;
}


double calculate_ic(string group)
{
    int n = group.length();

    if (n <= 1)
        return 0;

    int freq[26] = {0};

    for (char c : group)
        freq[c - 'A']++;

    int sum = 0;

    for (int i = 0; i < 26; i++)
        sum += freq[i] * (freq[i] - 1);

    return (double)sum / (n * (n - 1));
}


vector<string> split_into_groups(string text, int keyLength)
{
    vector<string> groups(keyLength);

    for (int i = 0; i < (int)text.length(); i++)
        groups[i % keyLength] += text[i];

    return groups;
}


void frequency_analysis(string group)
{
    int freq[26] = {0};

    for (char c : group)
        freq[c - 'A']++;

    for (int i = 0; i < 26; i++)
    {
        cout << char('A' + i) << ":" << freq[i] << " ";
    }

    cout << endl;
}


int find_shift(string group)
{
    double english[26] =
    {
        0.082, 0.015, 0.028, 0.043, 0.127, 0.022,
        0.020, 0.061, 0.070, 0.0015, 0.0077, 0.040,
        0.024, 0.067, 0.075, 0.019, 0.00095, 0.060,
        0.063, 0.091, 0.028, 0.0098, 0.024, 0.0015,
        0.020, 0.00074
    };

    int freq[26] = {0};

    for (char c : group)
        freq[c - 'A']++;

    int n = group.length();

    double bestScore = 1e100;
    int bestShift = 0;

    for (int shift = 0; shift < 26; shift++)
    {
        double score = 0;

        for (int i = 0; i < 26; i++)
        {
            int decryptedLetter = (i - shift + 26) % 26;

            double expected = english[decryptedLetter] * n;

            if (expected > 0)
            {
                double difference = freq[i] - expected;
                score += difference * difference / expected;
            }
        }

        if (score < bestScore)
        {
            bestScore = score;
            bestShift = shift;
        }
    }

    return bestShift;
}


string find_key(vector<string> groups)
{
    string key;

    for (string group : groups)
    {
        int shift = find_shift(group);
        key += char('A' + shift);
    }

    return key;
}


string vigenere_decrypt(string ciphertext, string key)
{
    string plaintext = "";

    for (int i = 0; i < (int)ciphertext.length(); i++)
    {
        int c = ciphertext[i] - 'A';
        int k = key[i % key.length()] - 'A';

        int p = (c - k + 26) % 26;

        plaintext += char('A' + p);
    }

    return plaintext;
}


string vigenere_encrypt(string plaintext, string key)
{
    string ciphertext = "";

    for (int i = 0; i < (int)plaintext.length(); i++)
    {
        int p = plaintext[i] - 'A';
        int k = key[i % key.length()] - 'A';

        int c = (p + k) % 26;

        ciphertext += char('A' + c);
    }

    return ciphertext;
}


bool verify(string original, string encrypted)
{
    return original == encrypted;
}

int main()
{
    ifstream file("ciphertext.txt");

    string input;
    string line;

    while (getline(file, line))
        input += line;

    string ciphertext = clean_ciphertext(input);

    cout << "Cleaned ciphertext:\n";
    cout << ciphertext << "\n";

   
    int keyLength = kasiski_analysis(ciphertext);

    cout << "\nEstimated key length: " << keyLength << endl;

   
    vector<string> groups = split_into_groups(ciphertext, keyLength);

    cout << "\nFrequency tables:\n";

    for (int i = 0; i < (int)groups.size(); i++)
    {
        cout << "\nGroup " << i + 1 << endl;

        frequency_analysis(groups[i]);

        cout << "IC = " << calculate_ic(groups[i]) << endl;
    }

   
    string key = find_key(groups);

    cout << "\nRecovered key: " << key << endl;

  
    string plaintext = vigenere_decrypt(ciphertext, key);

    cout << "\nRecovered plaintext:\n";
    cout << plaintext << endl;

  
    string encrypted = vigenere_encrypt(plaintext, key);

    cout << "\nVerification: ";

    if (verify(ciphertext, encrypted))
        cout << "SUCCESS - Re-encryption matches original ciphertext.\n";
    else
        cout << "FAILED - Re-encryption does not match.\n";

    return 0;
}
