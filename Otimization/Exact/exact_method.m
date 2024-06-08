clc;
clear;

% Load the data
Nodes = load("Nodefiles/Nodes200.txt");
Links = load("Nodefiles/Links200.txt");
L = load("Nodefiles/L200.txt");

% Number of nodes and links
n = size(Nodes, 1);
E = size(Links, 1);

% Create the graph
G = graph(L);

% Number of critical nodes
c = 8;

% Create the lpsolve file
fname = 'exact_model_c8.lpt';
fid = fopen(fname, 'wt');

% Critical Node Detection Algorithm

% First Step --> Minimize
% Calculate the number of connected node pairs
fprintf(fid, 'min ');
for i = 1:n-1
    for j = i+1:n
        fprintf(fid, '+ u%d_%d ', i, j);
    end
end

% Second Step --> Subject to
fprintf(fid,'\nsubject to\n');
% Number of critical nodes must be equal to c
for i = 1:n
    fprintf(fid, '+ v%d ', i);
end
fprintf(fid, '= %d\n', c);

% If i is not a critical node and j is also not a critical node, then nodes i and j are connected
for link = 1:E
    i = Links(link, 1);
    j = Links(link, 2);
    fprintf(fid, '+ u%d_%d + v%d + v%d >= 1\n', i, j, i, j);
end

%If i is connected with its neighbour k and k is connected with j, then node i is connected with node j
for i = 1:n
    for j = i+1:n
        i_neighbors = neighbors(G, i);
        if ismember(j, i_neighbors)
            continue;
        end
        for k_index = 1:length(i_neighbors)
            k = i_neighbors(k_index);
            fprintf(fid, '+ u%d_%d - u%d_%d - u%d_%d - v%d >= -1\n', i, j, min(i, k), max(i, k), min(k, j), max(k, j), k);
        end
    end
end

% Third Step --> Variable types
fprintf(fid, 'binary\n');
for i = 1:n
    fprintf(fid, 'v%d ', i);
end

fprintf(fid, '\ngeneral\n');
for i = 1:n-1
    for j = i+1:n
        fprintf(fid, 'u%d_%d ', i, j);
    end
end

fprintf(fid, '\nend');

fclose(fid);

fprintf('Model created successfully\n');