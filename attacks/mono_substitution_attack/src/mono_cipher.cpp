/*
 * CryptoLabX - Monoalphabetic Substitution Cipher & Cryptanalysis
 * Course  : Cryptography Laboratory (22CPP307)
 * Assignment 5: Frequency and Pattern Analysis
 * Group   : 10
 * Language: C++
 *
 * Functions implemented:
 *   1. frequency_analysis()
 *   2. word_frequency_analysis()
 *   3. pattern_analysis()
 *   4. apply_substitution()
 *   5. display_partial_plaintext()
 *   6. verify_solution()
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <set>
using namespace std;


// ============================================================
//                   GLOBAL DATA
// ============================================================

// Standard English letter frequencies (percentage)
double ENGLISH_FREQ[26] = {
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094,
    6.966, 0.153, 0.772, 4.025, 2.406,  6.749, 7.507, 1.929,
    0.095, 5.987, 6.327, 9.056, 2.758,  0.978, 2.360, 0.150,
    1.974, 0.074
};

string ENGLISH_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ";

// Current substitution mapping: substitution_map['A'] = 'X' means ciphertext A -> plaintext X
map<char, char> substitution_map;

// The encryption key used to create ciphertext
char encryption_key[26];


// ============================================================
//              UTILITY FUNCTIONS
// ============================================================

string to_upper(string s) {
    for (int i = 0; i < s.length(); i++) {
        if (s[i] >= 'a' && s[i] <= 'z')
            s[i] = s[i] - 'a' + 'A';
    }
    return s;
}

string to_lower(string s) {
    for (int i = 0; i < s.length(); i++) {
        if (s[i] >= 'A' && s[i] <= 'Z')
            s[i] = s[i] - 'A' + 'a';
    }
    return s;
}

bool is_alpha(char c) {
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
}

char to_upper_char(char c) {
    if (c >= 'a' && c <= 'z') return c - 'a' + 'A';
    return c;
}

string read_file(string path) {
    ifstream file(path.c_str());
    if (!file.is_open()) {
        cout << "  [!] Error: Cannot open file: " << path << endl;
        return "";
    }
    stringstream buffer;
    buffer << file.rdbuf();
    file.close();
    return buffer.str();
}

void write_file(string path, string content) {
    ofstream file(path.c_str());
    file << content;
    file.close();
}

// Extract only alphabetic words from text
vector<string> get_words(string text) {
    vector<string> words;
    string word = "";
    for (int i = 0; i < text.length(); i++) {
        if (is_alpha(text[i])) {
            word += to_upper_char(text[i]);
        } else {
            if (word.length() > 0) {
                words.push_back(word);
                word = "";
            }
        }
    }
    if (word.length() > 0) words.push_back(word);
    return words;
}

// Get the letter pattern of a word (e.g., HELLO -> 0.1.2.2.3, THAT -> 0.1.2.0)
string get_word_pattern(string word) {
    map<char, int> letter_map;
    string pattern = "";
    int next_num = 0;
    for (int i = 0; i < word.length(); i++) {
        char c = to_upper_char(word[i]);
        if (letter_map.find(c) == letter_map.end()) {
            letter_map[c] = next_num;
            next_num++;
        }
        if (i > 0) pattern += ".";
        // Convert int to string manually for older compilers
        int val = letter_map[c];
        if (val < 10) {
            pattern += (char)('0' + val);
        } else {
            pattern += (char)('0' + val / 10);
            pattern += (char)('0' + val % 10);
        }
    }
    return pattern;
}


// ============================================================
//            ENCRYPTION / DECRYPTION
// ============================================================

void generate_random_key() {
    // Create a random permutation of A-Z
    for (int i = 0; i < 26; i++) {
        encryption_key[i] = 'A' + i;
    }
    srand(time(0));
    for (int i = 25; i > 0; i--) {
        int j = rand() % (i + 1);
        char temp = encryption_key[i];
        encryption_key[i] = encryption_key[j];
        encryption_key[j] = temp;
    }
}

string encrypt_text(string plaintext) {
    string ciphertext = "";
    for (int i = 0; i < plaintext.length(); i++) {
        char c = plaintext[i];
        if (c >= 'A' && c <= 'Z') {
            ciphertext += encryption_key[c - 'A'];
        } else if (c >= 'a' && c <= 'z') {
            // Keep lowercase mapping
            char enc = encryption_key[c - 'a'];
            ciphertext += (char)(enc - 'A' + 'a');
        } else {
            ciphertext += c;
        }
    }
    return ciphertext;
}

string decrypt_with_key(string ciphertext, char key[26]) {
    // Build reverse mapping
    char reverse_key[26];
    for (int i = 0; i < 26; i++) {
        reverse_key[key[i] - 'A'] = 'A' + i;
    }
    string plaintext = "";
    for (int i = 0; i < ciphertext.length(); i++) {
        char c = ciphertext[i];
        if (c >= 'A' && c <= 'Z') {
            plaintext += reverse_key[c - 'A'];
        } else if (c >= 'a' && c <= 'z') {
            char dec = reverse_key[c - 'a'];
            plaintext += (char)(dec - 'A' + 'a');
        } else {
            plaintext += c;
        }
    }
    return plaintext;
}


// ============================================================
//       1. FREQUENCY ANALYSIS
// ============================================================

void frequency_analysis(string ciphertext) {
    int freq[26] = {0};
    int total = 0;

    for (int i = 0; i < ciphertext.length(); i++) {
        char c = to_upper_char(ciphertext[i]);
        if (c >= 'A' && c <= 'Z') {
            freq[c - 'A']++;
            total++;
        }
    }

    // Sort letters by frequency (descending)
    vector<pair<int, char> > sorted_freq;
    for (int i = 0; i < 26; i++) {
        sorted_freq.push_back(make_pair(freq[i], 'A' + i));
    }
    sort(sorted_freq.begin(), sorted_freq.end());
    reverse(sorted_freq.begin(), sorted_freq.end());

    cout << endl;
    cout << "  ============================================" << endl;
    cout << "       LETTER FREQUENCY ANALYSIS" << endl;
    cout << "  ============================================" << endl;
    cout << "  Total letters: " << total << endl;
    cout << endl;
    cout << "  " << left << setw(10) << "Letter"
         << setw(10) << "Count"
         << setw(12) << "Frequency%"
         << "  Bar" << endl;
    cout << "  " << string(50, '-') << endl;

    for (int i = 0; i < 26; i++) {
        char letter = sorted_freq[i].second;
        int count = sorted_freq[i].first;
        double pct = (total > 0) ? (count * 100.0 / total) : 0;

        // Visual bar
        int bar_len = (int)(pct / 0.5);
        string bar(bar_len, '#');

        cout << "  " << left << setw(10) << letter
             << setw(10) << count
             << fixed << setprecision(2) << setw(12) << pct
             << "  " << bar << endl;
    }

    // Show comparison with English
    cout << endl;
    cout << "  Ciphertext frequency order: ";
    for (int i = 0; i < 26; i++) cout << sorted_freq[i].second;
    cout << endl;
    cout << "  English frequency order   : " << ENGLISH_ORDER << endl;
    cout << endl;
    cout << "  Top 5 most frequent ciphertext letters:" << endl;
    for (int i = 0; i < 5 && i < 26; i++) {
        double pct = (total > 0) ? (sorted_freq[i].first * 100.0 / total) : 0;
        cout << "    " << sorted_freq[i].second << " (" << fixed << setprecision(1)
             << pct << "%) --> likely maps to English: " << ENGLISH_ORDER[i] << endl;
    }
}


// ============================================================
//       2. WORD FREQUENCY ANALYSIS
// ============================================================

void word_frequency_analysis(string ciphertext) {
    vector<string> words = get_words(ciphertext);

    // Count word frequencies
    map<string, int> word_count;
    for (int i = 0; i < words.size(); i++) {
        word_count[words[i]]++;
    }

    // Separate by word length
    vector<string> one_letter, two_letter, three_letter;
    for (map<string, int>::iterator it = word_count.begin(); it != word_count.end(); it++) {
        if (it->first.length() == 1) one_letter.push_back(it->first);
        else if (it->first.length() == 2) two_letter.push_back(it->first);
        else if (it->first.length() == 3) three_letter.push_back(it->first);
    }

    cout << endl;
    cout << "  ============================================" << endl;
    cout << "       WORD FREQUENCY ANALYSIS" << endl;
    cout << "  ============================================" << endl;
    cout << "  Total words: " << words.size() << endl;

    // One-letter words (must be A or I in English)
    cout << endl << "  ONE-LETTER WORDS (English: only A or I):" << endl;
    cout << "  " << string(40, '-') << endl;
    for (int i = 0; i < one_letter.size(); i++) {
        cout << "    " << one_letter[i] << "  (appears " << word_count[one_letter[i]] << " times)" << endl;
    }
    if (one_letter.empty()) cout << "    (none found)" << endl;

    // Two-letter words
    cout << endl << "  TWO-LETTER WORDS (English: OF, TO, IN, IS, IT, etc.):" << endl;
    cout << "  " << string(40, '-') << endl;
    // Sort by frequency
    vector<pair<int, string> > two_sorted;
    for (int i = 0; i < two_letter.size(); i++) {
        two_sorted.push_back(make_pair(word_count[two_letter[i]], two_letter[i]));
    }
    sort(two_sorted.begin(), two_sorted.end());
    reverse(two_sorted.begin(), two_sorted.end());
    for (int i = 0; i < two_sorted.size(); i++) {
        cout << "    " << two_sorted[i].second << "  (appears " << two_sorted[i].first << " times)" << endl;
    }

    // Three-letter words
    cout << endl << "  THREE-LETTER WORDS (English: THE, AND, FOR, ARE, etc.):" << endl;
    cout << "  " << string(40, '-') << endl;
    vector<pair<int, string> > three_sorted;
    for (int i = 0; i < three_letter.size(); i++) {
        three_sorted.push_back(make_pair(word_count[three_letter[i]], three_letter[i]));
    }
    sort(three_sorted.begin(), three_sorted.end());
    reverse(three_sorted.begin(), three_sorted.end());
    for (int i = 0; i < min((int)three_sorted.size(), 10); i++) {
        cout << "    " << three_sorted[i].second << "  (appears " << three_sorted[i].first << " times)" << endl;
    }

    // Most repeated words overall
    cout << endl << "  TOP 15 MOST FREQUENT WORDS:" << endl;
    cout << "  " << string(40, '-') << endl;
    vector<pair<int, string> > all_sorted;
    for (map<string, int>::iterator it = word_count.begin(); it != word_count.end(); it++) {
        all_sorted.push_back(make_pair(it->second, it->first));
    }
    sort(all_sorted.begin(), all_sorted.end());
    reverse(all_sorted.begin(), all_sorted.end());
    for (int i = 0; i < min((int)all_sorted.size(), 15); i++) {
        cout << "    " << left << setw(15) << all_sorted[i].second << "  x" << all_sorted[i].first << endl;
    }
}


// ============================================================
//       3. PATTERN ANALYSIS
// ============================================================

void pattern_analysis(string ciphertext) {
    vector<string> words = get_words(ciphertext);

    // Find words with repeated letter patterns
    map<string, vector<string> > pattern_groups;
    for (int i = 0; i < words.size(); i++) {
        string pattern = get_word_pattern(words[i]);
        // Only track interesting patterns (with repeats)
        bool has_repeat = false;
        map<char, int> char_count;
        for (int j = 0; j < words[i].length(); j++) {
            char_count[words[i][j]]++;
            if (char_count[words[i][j]] > 1) has_repeat = true;
        }
        pattern_groups[pattern].push_back(words[i]);
    }

    cout << endl;
    cout << "  ============================================" << endl;
    cout << "       PATTERN ANALYSIS" << endl;
    cout << "  ============================================" << endl;
    cout << "  Patterns help identify words with repeated letters." << endl;
    cout << "  Example: THAT has pattern 0.1.2.0 (T repeats)" << endl;
    cout << "           HELLO has pattern 0.1.2.2.3 (L repeats)" << endl;
    cout << endl;

    // Show unique patterns with repeated letters
    cout << "  WORDS WITH REPEATED LETTER PATTERNS:" << endl;
    cout << "  " << string(50, '-') << endl;

    for (map<string, vector<string> >::iterator it = pattern_groups.begin();
         it != pattern_groups.end(); it++) {
        // Deduplicate words for this pattern
        set<string> unique_words(it->second.begin(), it->second.end());
        // Check if pattern has repeats
        string pat = it->first;
        map<string, int> pat_nums;
        bool has_repeat = false;
        stringstream ss(pat);
        string token;
        while (getline(ss, token, '.')) {
            pat_nums[token]++;
            if (pat_nums[token] > 1) has_repeat = true;
        }
        if (has_repeat && unique_words.size() > 0) {
            cout << "    Pattern " << left << setw(20) << pat << ": ";
            for (set<string>::iterator w = unique_words.begin(); w != unique_words.end(); w++) {
                cout << *w << " ";
            }
            cout << endl;
        }
    }

    // Common English patterns to look for
    cout << endl;
    cout << "  COMMON ENGLISH WORD PATTERNS:" << endl;
    cout << "  " << string(50, '-') << endl;
    cout << "    THE  -> pattern 0.1.2 (all different letters)" << endl;
    cout << "    THAT -> pattern 0.1.2.0 (first = last)" << endl;
    cout << "    WILL -> pattern 0.1.2.2 (last two same)" << endl;
    cout << "    ALL  -> pattern 0.1.1 (last two same)" << endl;
    cout << "    SEE  -> pattern 0.1.1 (last two same)" << endl;
}


// ============================================================
//       4. APPLY SUBSTITUTION
// ============================================================

void apply_substitution(char cipher_letter, char plain_letter) {
    cipher_letter = to_upper_char(cipher_letter);
    plain_letter = to_upper_char(plain_letter);

    // Check if this plain letter is already assigned
    for (map<char, char>::iterator it = substitution_map.begin();
         it != substitution_map.end(); it++) {
        if (it->second == plain_letter && it->first != cipher_letter) {
            cout << "  [!] Warning: '" << plain_letter << "' is already mapped from '"
                 << it->first << "'. Removing old mapping." << endl;
            substitution_map.erase(it);
            break;
        }
    }

    substitution_map[cipher_letter] = plain_letter;
    cout << "  [+] Substitution added: " << cipher_letter
         << " --> " << plain_letter << endl;
    cout << "  Total mappings so far: " << substitution_map.size() << "/26" << endl;
}


// ============================================================
//       5. DISPLAY PARTIAL PLAINTEXT
// ============================================================

void display_partial_plaintext(string ciphertext, bool show_full = false) {
    cout << endl;
    cout << "  ============================================" << endl;
    if (show_full) {
        cout << "       FULL PARTIAL PLAINTEXT" << endl;
    } else {
        cout << "       PARTIAL PLAINTEXT PREVIEW (Clean View)" << endl;
    }
    cout << "  ============================================" << endl;

    string result = "";
    int solved = 0, total_letters = 0;

    for (int i = 0; i < ciphertext.length(); i++) {
        char c = to_upper_char(ciphertext[i]);
        if (c >= 'A' && c <= 'Z') {
            total_letters++;
            if (substitution_map.find(c) != substitution_map.end()) {
                result += substitution_map[c];
                solved++;
            } else {
                result += '.';
            }
        } else {
            result += ciphertext[i];
        }
    }

    // Print lines of 70 characters (only first 3 lines if not show_full)
    int line_len = 70;
    int lines_printed = 0;
    int max_lines = show_full ? 9999 : 3;

    for (int i = 0; i < result.length(); i += line_len) {
        if (lines_printed >= max_lines) {
            cout << "  ... [showing first 3 lines preview for clear view] ..." << endl << endl;
            break;
        }
        string line_ct = ciphertext.substr(i, min(line_len, (int)ciphertext.length() - i));
        string line_pt = result.substr(i, min(line_len, (int)result.length() - i));
        cout << "  CT: " << line_ct << endl;
        cout << "  PT: " << line_pt << endl;
        cout << endl;
        lines_printed++;
    }

    double pct = (total_letters > 0) ? (solved * 100.0 / total_letters) : 0;
    cout << "  Progress: " << solved << "/" << total_letters
         << " letters solved (" << fixed << setprecision(1) << pct << "%)" << endl;
    cout << "  Unique letters mapped: " << substitution_map.size() << "/26" << endl;

    // Show current substitution table
    cout << endl << "  Current Substitution Map:" << endl;
    cout << "  Cipher: ";
    for (char c = 'A'; c <= 'Z'; c++) cout << c << " ";
    cout << endl << "  Plain : ";
    for (char c = 'A'; c <= 'Z'; c++) {
        if (substitution_map.find(c) != substitution_map.end())
            cout << substitution_map[c] << " ";
        else
            cout << ". ";
    }
    cout << endl;
}


// ============================================================
//       6. VERIFY SOLUTION
// ============================================================

void verify_solution(string original_plaintext, string ciphertext) {
    cout << endl;
    cout << "  ============================================" << endl;
    cout << "       VERIFICATION" << endl;
    cout << "  ============================================" << endl;

    // Build recovered key from substitution_map (reverse: cipher -> plain)
    char recovered_key[26];
    bool key_complete = true;
    for (int i = 0; i < 26; i++) {
        char cipher_letter = 'A' + i;
        bool found = false;
        for (map<char, char>::iterator it = substitution_map.begin();
             it != substitution_map.end(); it++) {
            if (it->second == cipher_letter) {
                // it->first is the cipher letter that maps to plain letter cipher_letter
                // Actually we need: for each plain letter, what cipher letter was used
            }
        }
    }

    // Build forward key: plain letter -> cipher letter
    // substitution_map stores cipher->plain, so reverse it
    cout << "  Recovered Decryption Key:" << endl;
    cout << "  Cipher: ";
    for (char c = 'A'; c <= 'Z'; c++) cout << c << " ";
    cout << endl << "  Plain : ";
    for (char c = 'A'; c <= 'Z'; c++) {
        if (substitution_map.find(c) != substitution_map.end())
            cout << substitution_map[c] << " ";
        else {
            cout << "? ";
            key_complete = false;
        }
    }
    cout << endl;

    if (!key_complete) {
        cout << endl << "  [!] Key is not complete yet. Continue adding substitutions." << endl;
        return;
    }

    // Decrypt ciphertext using recovered map
    string recovered_text = "";
    for (int i = 0; i < ciphertext.length(); i++) {
        char c = ciphertext[i];
        char upper = to_upper_char(c);
        if (upper >= 'A' && upper <= 'Z') {
            char plain = substitution_map[upper];
            if (c >= 'a' && c <= 'z')
                recovered_text += (char)(plain - 'A' + 'a');
            else
                recovered_text += plain;
        } else {
            recovered_text += c;
        }
    }

    // Compare with original
    string orig_upper = to_upper(original_plaintext);
    string recv_upper = to_upper(recovered_text);

    int match = 0, total = 0;
    for (int i = 0; i < min(orig_upper.length(), recv_upper.length()); i++) {
        if (is_alpha(orig_upper[i])) {
            total++;
            if (orig_upper[i] == recv_upper[i]) match++;
        }
    }

    double accuracy = (total > 0) ? (match * 100.0 / total) : 0;
    cout << endl;
    cout << "  Accuracy: " << match << "/" << total << " letters correct ("
         << fixed << setprecision(1) << accuracy << "%)" << endl;

    if (accuracy > 99.0) {
        cout << "  [+] SUCCESS! Plaintext fully recovered!" << endl;
    } else if (accuracy > 80.0) {
        cout << "  [~] Almost there! A few substitutions may be wrong." << endl;
    } else {
        cout << "  [!] Many letters incorrect. Continue refining substitutions." << endl;
    }

    // Show actual encryption key vs recovered
    cout << endl << "  Actual Encryption Key Used:" << endl;
    cout << "  Plain : ";
    for (char c = 'A'; c <= 'Z'; c++) cout << c << " ";
    cout << endl << "  Cipher: ";
    for (int i = 0; i < 26; i++) cout << encryption_key[i] << " ";
    cout << endl;

    // Re-encrypt with recovered key to validate
    cout << endl << "  First 100 chars of recovered plaintext:" << endl;
    cout << "  " << recovered_text.substr(0, 100) << endl;
    cout << endl << "  First 100 chars of original plaintext:" << endl;
    cout << "  " << original_plaintext.substr(0, 100) << endl;
}


// ============================================================
//       AUTO-SOLVE (Frequency-based initial guess)
// ============================================================

void auto_frequency_solve(string ciphertext) {
    // Count frequencies
    int freq[26] = {0};
    int total = 0;
    for (int i = 0; i < ciphertext.length(); i++) {
        char c = to_upper_char(ciphertext[i]);
        if (c >= 'A' && c <= 'Z') {
            freq[c - 'A']++;
            total++;
        }
    }

    // Sort by frequency descending
    vector<pair<int, char> > sorted_freq;
    for (int i = 0; i < 26; i++) {
        sorted_freq.push_back(make_pair(freq[i], 'A' + i));
    }
    sort(sorted_freq.begin(), sorted_freq.end());
    reverse(sorted_freq.begin(), sorted_freq.end());

    // Map most frequent cipher letter -> most frequent English letter
    substitution_map.clear();
    for (int i = 0; i < 26; i++) {
        substitution_map[sorted_freq[i].second] = ENGLISH_ORDER[i];
    }

    cout << "  [+] Auto-applied frequency-based substitution for all 26 letters." << endl;
    cout << "  This is an initial guess -- you can refine it manually." << endl;
}


// ============================================================
//                     MAIN MENU
// ============================================================

int main() {
    string plaintext_path = "plaintext/source_text.txt";
    string ciphertext_path = "outputs/ciphertext.txt";

    string plaintext = "";
    string ciphertext = "";

    cout << endl;
    cout << "  ======================================================" << endl;
    cout << "    CryptoLabX - Monoalphabetic Cipher Cryptanalysis" << endl;
    cout << "    Course: Cryptography Laboratory (22CPP307)" << endl;
    cout << "    Assignment 5  |  Group 10  |  C++" << endl;
    cout << "  ======================================================" << endl;

    // Load plaintext
    plaintext = read_file(plaintext_path);
    if (plaintext.empty()) {
        cout << "  [!] Failed to load plaintext. Exiting." << endl;
        return 1;
    }
    cout << "  [+] Loaded plaintext (" << plaintext.length() << " characters)" << endl;

    // Generate random key and encrypt
    generate_random_key();
    ciphertext = encrypt_text(plaintext);

    // Save ciphertext
    write_file(ciphertext_path, ciphertext);
    cout << "  [+] Ciphertext generated and saved to: " << ciphertext_path << endl;

    // Show encryption key (hidden from analyst in real scenario)
    cout << endl << "  Encryption Key (for verification only):" << endl;
    cout << "  Plain : ";
    for (char c = 'A'; c <= 'Z'; c++) cout << c << " ";
    cout << endl << "  Cipher: ";
    for (int i = 0; i < 26; i++) cout << encryption_key[i] << " ";
    cout << endl;

    // Interactive menu
    while (true) {
        cout << endl;
        cout << "  ======================================================" << endl;
        cout << "    CRYPTANALYSIS MENU" << endl;
        cout << "  ======================================================" << endl;
        cout << "  [1] Letter Frequency Analysis" << endl;
        cout << "  [2] Word Frequency Analysis" << endl;
        cout << "  [3] Pattern Analysis (Repeated Letters)" << endl;
        cout << "  [4] Add Substitution (Cipher -> Plain)" << endl;
        cout << "  [5] Remove Substitution" << endl;
        cout << "  [6] View Partial Plaintext" << endl;
        cout << "  [7] Auto-Solve (Frequency Guess)" << endl;
        cout << "  [8] Verify Solution" << endl;
        cout << "  [9] Reset All Substitutions" << endl;
        cout << "  [0] Exit" << endl;
        cout << "  ======================================================" << endl;
        cout << "  Choose option: ";

        string choice;
        getline(cin, choice);

        if (choice == "1") {
            frequency_analysis(ciphertext);

        } else if (choice == "2") {
            word_frequency_analysis(ciphertext);

        } else if (choice == "3") {
            pattern_analysis(ciphertext);

        } else if (choice == "4") {
            char cl, pl;
            cout << "  Enter cipher letter: ";
            cin >> cl;
            cout << "  Maps to plain letter: ";
            cin >> pl;
            cin.ignore();
            apply_substitution(cl, pl);
            display_partial_plaintext(ciphertext);

        } else if (choice == "5") {
            char cl;
            cout << "  Enter cipher letter to remove: ";
            cin >> cl;
            cin.ignore();
            cl = to_upper_char(cl);
            if (substitution_map.find(cl) != substitution_map.end()) {
                substitution_map.erase(cl);
                cout << "  [+] Removed mapping for " << cl << endl;
            } else {
                cout << "  [!] No mapping exists for " << cl << endl;
            }

        } else if (choice == "6") {
            display_partial_plaintext(ciphertext);

        } else if (choice == "7") {
            auto_frequency_solve(ciphertext);
            display_partial_plaintext(ciphertext);

        } else if (choice == "8") {
            verify_solution(plaintext, ciphertext);

        } else if (choice == "9") {
            substitution_map.clear();
            cout << "  [+] All substitutions cleared." << endl;

        } else if (choice == "0") {
            cout << "  Goodbye!" << endl;
            break;

        } else {
            cout << "  [!] Invalid option. Enter 0-9." << endl;
        }
    }

    return 0;
}
