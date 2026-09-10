#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cmath>
#include <cctype>

using namespace std;



// 1. Clean ciphertext

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



// 2. Find repeated 3-letter patterns

vector<string> find_repeated_patterns(string text)
{
    vector<string> patterns;

    for (int i = 0; i <= (int)text.length() - 3; i++)
    {
        string pattern = text.substr(i, 3);

        bool repeated = false;

        for (int j = i + 3; j <= (int)text.length() - 3; j++)
        {
            if (text.substr(j, 3) == pattern)
            {
                repeated = true;
                break;
            }
        }

        if (repeated)
        {
            bool already_present = false;

            for (string p : patterns)
            {
                if (p == pattern)
                {
                    already_present = true;
                    break;
                }
            }

            if (!already_present)
                patterns.push_back(pattern);
        }
    }

    return patterns;
}



// 3. Calculate distances

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



// 4. Find factors

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



// 5. Kasiski analysis
// Returns candidate key lengths

vector<int> kasiski_analysis(string text)
{
    vector<string> patterns = find_repeated_patterns(text);

    map<int, int> factor_count;

    cout << "\nKASISKI ANALYSIS\n";

    for (string pattern : patterns)
    {
        vector<int> distances = calculate_distances(text, pattern);

        cout << "Pattern " << pattern << " : ";

        for (int d : distances)
        {
            cout << d << " ";

            vector<int> factors = find_factors(d);

            for (int f : factors)
                factor_count[f]++;
        }

        cout << endl;
    }

    // Sort factors according to frequency
    vector<pair<int, int>> factors;

    for (auto x : factor_count)
        factors.push_back(x);

    sort(factors.begin(), factors.end(),
         [](pair<int, int> a, pair<int, int> b)
         {
             return a.second > b.second;
         });

    cout << "\nKasiski candidate key lengths:\n";

    vector<int> candidates;

    for (int i = 0; i < (int)factors.size() && i < 8; i++)
    {
        cout << factors[i].first
             << " (count = "
             << factors[i].second
             << ")\n";

        candidates.push_back(factors[i].first);
    }

    return candidates;
}



// 6. Calculate Index of Coincidence

double calculate_ic(string group)
{
    int n = group.length();

    if (n <= 1)
        return 0.0;

    int frequency[26] = {0};

    for (char c : group)
        frequency[c - 'A']++;

    int numerator = 0;

    for (int i = 0; i < 26; i++)
        numerator += frequency[i] * (frequency[i] - 1);

    return (double)numerator / (n * (n - 1));
}



// 7. Split ciphertext into groups

vector<string> split_into_groups(string text, int keyLength)
{
    vector<string> groups(keyLength);

    for (int i = 0; i < (int)text.length(); i++)
    {
        groups[i % keyLength] += text[i];
    }

    return groups;
}



// 8. Frequency analysis

void frequency_analysis(string group)
{
    int frequency[26] = {0};

    for (char c : group)
        frequency[c - 'A']++;

    for (int i = 0; i < 26; i++)
    {
        cout << char('A' + i)
             << ":" << frequency[i] << " ";
    }

    cout << endl;
}



// 9. Find Caesar shift

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

    int frequency[26] = {0};

    for (char c : group)
        frequency[c - 'A']++;

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
                double difference = frequency[i] - expected;

                score += (difference * difference) / expected;
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



// 10. Find probable key

string find_key(vector<string> groups)
{
    string key = "";

    for (string group : groups)
    {
        int shift = find_shift(group);

        key += char('A' + shift);
    }

    return key;
}



// 11. Vigenere decryption

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



// 12. Vigenere encryption

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



// 13. Verify

bool verify(string original, string encrypted)
{
    return original == encrypted;
}


int main()
{
    // Read ciphertext
    ifstream file("ciphertext.txt");

    string input;
    string line;

    while (getline(file, line))
    {
        input += line;
    }

    file.close();


    // Step 1: Clean ciphertext
    string ciphertext = clean_ciphertext(input);

    cout << "CLEANED CIPHERTEXT\n";
    cout << ciphertext << "\n";

    cout << "\nTotal characters: "
         << ciphertext.length() << endl;


    // Step 2: Kasiski
    vector<int> candidates = kasiski_analysis(ciphertext);


    // If no candidates were found
    if (candidates.empty())
    {
        cout << "\nNo Kasiski candidates found.\n";
        return 0;
    }


    // Step 3: Use IC to select correct key length
    cout << "\nINDEX OF COINCIDENCE\n";

    int bestKeyLength = candidates[0];

    double bestDifference = 100.0;

    for (int keyLength : candidates)
    {
        vector<string> groups =
            split_into_groups(ciphertext, keyLength);

        double totalIC = 0.0;

        for (string group : groups)
        {
            totalIC += calculate_ic(group);
        }

        double averageIC =
            totalIC / groups.size();

        // English IC is approximately 0.066
        double difference =
            abs(averageIC - 0.066);

        cout << "Key length "
             << keyLength
             << " -> Average IC = "
             << averageIC
             << endl;

        if (difference < bestDifference)
        {
            bestDifference = difference;
            bestKeyLength = keyLength;
        }
    }


    cout << "\nSelected key length using IC: "
         << bestKeyLength << endl;


    // Step 4: Split using selected key length
    vector<string> groups =
        split_into_groups(ciphertext, bestKeyLength);


    // Step 5: Frequency analysis
    cout << "\nFREQUENCY ANALYSIS\n";

    for (int i = 0; i < (int)groups.size(); i++)
    {
        cout << "\nGroup " << i + 1 << endl;

        cout << "Text: "
             << groups[i] << endl;

        cout << "Frequency:\n";

        frequency_analysis(groups[i]);

        cout << "IC = "
             << calculate_ic(groups[i])
             << endl;
    }


    // Step 6: Find key
    string key = find_key(groups);

    cout << "\nRECOVERED KEY\n";
    cout << key << endl;


    // Step 7: Decrypt
    string plaintext =
        vigenere_decrypt(ciphertext, key);

    cout << "\nRECOVERED PLAINTEXT\n";
    cout << plaintext << endl;


    // Step 8: Re-encrypt
    string encrypted =
        vigenere_encrypt(plaintext, key);


    // Step 9: Verify
    cout << "\nVERIFICATION\n";

    if (verify(ciphertext, encrypted))
    {
        cout << "SUCCESS\n";
        cout << "Re-encrypted ciphertext matches original ciphertext.\n";
    }
    else
    {
        cout << "FAILED\n";
        cout << "Re-encrypted ciphertext does not match original ciphertext.\n";
    }


    return 0;
}
