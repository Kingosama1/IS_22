#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    ifstream file("Horizontal_Format.csv");

    vector<vector<string>> transactions;

    string line;

    getline(file, line);

    while (getline(file, line))
    {
        stringstream stream(line);

        string tid, items;

        getline(stream, tid, ',');
        getline(stream, items);
        
        if (items.size() >= 2 &&
            items.front() == '"' &&
            items.back() == '"')
        {
            items = items.substr(1, items.size() - 2);
        }
        stringstream itemStream(items);

        string item;
        vector<string> transaction;

        while (getline(itemStream, item, ','))
        {
            transaction.push_back(item);
        }

        transactions.push_back(transaction);
    }

    return 0;
}