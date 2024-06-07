
function [best_solution,generation_count,time_found,exec_time] = GA(G,n,population_size,mutation_prob,m,end_time)    
    generation_count = 1;
    start_time = tic;
    nNodes = numnodes(G); % Numero de nos do grafo G
    population = zeros(population_size, n+1);

    for i = 1:population_size
         nodes = randperm(nNodes,n);
        population(i,:) = [nodes ConnectedNP(G,nodes)];
    end
    while toc(start_time) < end_time
        generation_count = generation_count + 1;
        % Ordenar a populacao pela ultima coluna (valores objetivos da pop)
        population = sortrows(population, n+1);
        new_population = zeros(population_size, n+1);  % nova populacao 
 
        for i = 1:population_size
            s = crossover(population, n);
            if(rand() < mutation_prob)
               s = mutation(s, G);
            end
            % P´ = P´ U {s} adicionando o fitness value na ultima linha
            new_population(i,:) = [s ConnectedNP(G,s)];
        end
        new_population = sortrows(new_population, n+1);
        if(new_population(1,end) < population(1,end))
            time_found = toc(start_time);
        end
        combined_population = [population(1:m,:); new_population];
        sortrows(combined_population, n+1);
        population = combined_population(1:end-m,:);

    end
    best_solution = population(1,end);
    exec_time = toc(start_time);
end