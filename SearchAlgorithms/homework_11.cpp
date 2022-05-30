#include <iostream>
#include <cstdio>
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <cstdlib>
#include <utility>
#include <set>
#include <queue>
#include <stack>
#include <cmath>
#include <unordered_map>
using namespace std;
struct State{
    int x, y, z;
};

struct Node{
    struct State* state;
    int path;
    int future;
    struct Node *parent;
};

struct State *dimension, *entrypoint, *exitpoint;
vector<vector<int>> operations;
map<string,vector<int>> actions;

struct State* allocateState(){
    struct State* state = (struct State*)malloc(sizeof(struct State));
    state->x = -1;
    state->y = -1;
    state->z = -1;
    return state;
}

struct Node* allocateNode(){
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->parent = NULL;
    node->path = 0;
    node->future = 0;
    node->state = NULL;
    return node;
}

struct State* getState(string dim){
    struct State *dimension = allocateState();
    istringstream iss(dim);
    string data;
    iss >> data; dimension->x = stoi(data);
    iss >> data; dimension->y = stoi(data);
    iss >> data; dimension->z = stoi(data);
    return dimension;
}

void getNode(string input){
    istringstream iss(input);
    string data, key;
    iss >> data; key = data;
    iss >> data; key += "#" + data;
    iss >> data; key += "#" + data;
    while( iss >> data){
        actions[key].push_back(stoi(data));
    }
}

bool boundaryTest(struct State* state){
    return (state->x < dimension->x && state->x >= 0) &&
           (state->y < dimension->y && state->y >= 0) &&
           (state->z < dimension->z && state->z >= 0);
}

bool goalTest(struct State* state){
    return (state->x == exitpoint->x) &&
           (state->y == exitpoint->y) &&
           (state->z == exitpoint->z);
}

string getStateAsString(struct State* state){
    return to_string(state->x) + "#" + to_string(state->y) + "#" + to_string(state->z);
}

int euclidianDistance(struct State* state){
    int dx = state->x - exitpoint->x;
    int dy = state->y - exitpoint->y;
    int dz = state->z - exitpoint->z;
    
    return (int)sqrt(dx*dx + dy*dy + dz*dz);
}

bool printSolution(struct Node* node){
    cout << node->path << endl;
    stack<struct Node*> sol; sol.push(node);
    while( node->parent != NULL){
        node = node->parent;
        sol.push(node);
    }
    cout << sol.size() << endl;
    int prevCost = 0;
    while(!sol.empty()){
        node = sol.top();sol.pop();
        cout << node->state->x << " " << node->state->y << " " << node->state->z <<" " << node->path - prevCost;
        prevCost = node->path;
        if(!sol.empty())
            cout << endl;
    }
    return true;
}

bool solveBFS(struct Node* enter){
    
    if(goalTest(enter->state)){
        return printSolution(enter);
    }
    
    queue<struct Node*> frontier; frontier.push(enter);
    struct State* state;
    string key;
    set<string> explored;
    
    while(!frontier.empty()){
        
        struct Node* node = frontier.front(); frontier.pop();
        state = node->state;
        key = getStateAsString(state);
        explored.insert(key);
        vector<int> action = actions[key];
        
        for(int j=0;j<action.size();j++){
            
            int operation = action[j];
            struct State* newState = allocateState();
            newState->x = state->x + operations[operation][0];
            newState->y = state->y + operations[operation][1];
            newState->z = state->z + operations[operation][2];
            
            key = getStateAsString(newState);
            if( boundaryTest(newState)==false  || explored.find(key)!=explored.end()) continue;
            
            struct Node* newNode = allocateNode();
            newNode->state = newState;
            newNode->path = node->path + 1;
            newNode->parent = node;
            
            if(goalTest(newState)){
                return printSolution(newNode);
            }
            
            frontier.push(newNode);explored.insert(key);
            
        }
    }
    return false;
}

bool solveUCS(struct Node* enter){
    
    if(goalTest(enter->state))
        return printSolution(enter);
    
    unordered_map<string, int> mp;
    
    priority_queue< pair<int,struct Node*>, vector<pair<int,struct Node*>>, greater<pair<int,struct Node*>> > frontier;
    frontier.push({0,enter});
    struct State* state;
    string key;
    int weight, stepCost;
    set<string> explored;
    
    while(!frontier.empty()){
        
        pair<int,struct Node*> p = frontier.top(); frontier.pop();
        weight = p.first;
        struct Node* node = p.second;
        state = node->state;
        if(goalTest(state)){
            return printSolution(node);
        }
        
        key = getStateAsString(state);
        explored.insert(key);
        vector<int> action = actions[key];
        
        for(int j=0;j<action.size();j++){
            
            int operation = action[j];
            struct State* newState = allocateState();
            newState->x = state->x + operations[operation][0];
            newState->y = state->y + operations[operation][1];
            newState->z = state->z + operations[operation][2];
            
            key = getStateAsString(newState);
            if( boundaryTest(newState)==false  || explored.find(key)!=explored.end()) continue;
            
            if(operation > 6)
                stepCost = 14;
            else
                stepCost = 10;
            
            struct Node* newNode = allocateNode();
            newNode->state = newState;
            newNode->path = node->path + stepCost;
            newNode->parent = node;
            
            if(mp.find(key) != mp.end() && mp[key] <= newNode->path) continue;
            
            mp[key] = newNode->path;
            frontier.push({newNode->path,newNode});//explored.insert(key);
            
        }
    }
    return false;
}

bool solveAstar(struct Node* enter){
    
    if(goalTest(enter->state))
        return printSolution(enter);
    
    unordered_map<string, int> mp;
    
    priority_queue< pair<int,struct Node*>, vector<pair<int,struct Node*>>, greater<pair<int,struct Node*>> > frontier;
    frontier.push({0,enter});
    struct State* state;
    string key;
    int weight, stepCost, futureCost;
    set<string> explored;
    
    while(!frontier.empty()){
        
        pair<int,struct Node*> p = frontier.top(); frontier.pop();
        weight = p.first;
        struct Node* node = p.second;
        state = node->state;
        if(goalTest(state)){
            return printSolution(node);
        }
        
        key = getStateAsString(state);
        explored.insert(key);
        vector<int> action = actions[key];
        
        for(int j=0;j<action.size();j++){
            
            int operation = action[j];
            struct State* newState = allocateState();
            newState->x = state->x + operations[operation][0];
            newState->y = state->y + operations[operation][1];
            newState->z = state->z + operations[operation][2];
            
            key = getStateAsString(newState);
            if( boundaryTest(newState)==false  || explored.find(key)!=explored.end()) continue;
            
            if(operation > 6)
                stepCost = 14;
            else
                stepCost = 10;
            
            futureCost = euclidianDistance(newState);
            
            struct Node* newNode = allocateNode();
            newNode->state = newState;
            newNode->path = node->path + stepCost;
            newNode->parent = node;
            
            if(mp.find(key) != mp.end() && mp[key] <= newNode->path) continue;
            
            mp[key] = newNode->path;
            frontier.push({newNode->path+futureCost,newNode});//explored.insert(key);
            
        }
    }
    return false;
}

void initialize(){
    operations.push_back({0,0,0});  //0
    operations.push_back({1,0,0});  //1
    operations.push_back({-1,0,0}); //2
    operations.push_back({0,1,0});  //3
    operations.push_back({0,-1,0}); //4
    operations.push_back({0,0,1});  //5
    operations.push_back({0,0,-1}); //6
    
    operations.push_back({1,1,0});   //7
    operations.push_back({1,-1,0});  //8
    operations.push_back({-1,1,0});  //9
    operations.push_back({-1,-1,0}); //10
    
    operations.push_back({1,0,1});   //11
    operations.push_back({1,0,-1});  //12
    operations.push_back({-1,0,1});  //13
    operations.push_back({-1,0,-1}); //14
    
    operations.push_back({0,1,1});   //15
    operations.push_back({0,1,-1});  //16
    operations.push_back({0,-1,1});  //17
    operations.push_back({0,-1,-1}); //18
}


int main() {
    initialize() ;
    FILE *fp = freopen("input.txt","r",stdin);
    FILE *fout = freopen("output.txt","w",stdout);
    string algo;
    getline(cin,algo);
    //cout << "algo is: " << algo << endl;
    string dim; getline(cin, dim);
    dimension = getState(dim);
    //cout << "Dimension: " << dimension->x << " " << dimension->y << " " << dimension->z <<  endl;
    string entry; getline(cin,entry);
    entrypoint = getState(entry);
    //cout << "Enter: " << entrypoint->x << " " << entrypoint->y << " " << entrypoint->z <<  endl;
    string finish; getline(cin,finish);
    exitpoint = getState(finish);
    //cout << "Exit: " << exitpoint->x << " " << exitpoint->y << " " << exitpoint->z <<  endl;
    string cases; getline(cin,cases);
    int test = stoi(cases);
    //cout << "cases: "<< test << endl;
    
    while(test--){
        string input; getline(cin,input);
        getNode(input);
    }
    
   
    /*cout << actions.size() << endl;
    for(auto it: actions){
        string key = it.first;
        cout << key << " ";
        vector<int> action = it.second;
        for(int j=0;j<action.size();j++){
            cout << action[j] << " ";
        }
        cout << endl;
    }*/
    /*cout << nodes.size() << endl;
    for(int i=0;i<nodes.size();i++){
        struct Node node = nodes[i];
        cout << node.state.x << " " << node.state.y << " " << node.state.z << " ";
        string key = to_string(node.state.x) + "#" + to_string(node.state.y) + "#" + to_string(node.state.z);
        vector<int> action = actions[key];
        for(int j=0;j<action.size();j++){
            cout << action[j] << " ";
        }
        cout << endl;
    }*/
    
    struct Node* enter = allocateNode();
    enter->state = entrypoint;
    bool flag = true;
    
    if(algo.compare("A*") == 0){
        flag = solveAstar(enter);
    }
    else if (algo.compare("UCS") == 0){
        flag = solveUCS(enter);
    }
    else{
        flag = solveBFS(enter);
    }
    if(flag == false)
            cout << "FAIL" << endl;
    fclose(fp);
    fclose(fout);
    return 0;
}
