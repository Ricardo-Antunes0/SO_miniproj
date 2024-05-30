function offspring = crossover(population, n)
    population_size = size(population,1);
  
    % Tournament selection for parent 1
    parent1_index1 = randi(population_size);
    parent1_index2 = randi(population_size);

    if(population(parent1_index1,end) < population(parent1_index2,end))
        parent1 = population(parent1_index1, 1:end-1);
    else
        parent1 = population(parent1_index2, 1:end-1);
    end

    % Tournament selection for parent 2
    parent2_index1 = randi(population_size);
    parent2_index2 = randi(population_size);       
    if(population(parent2_index1,end) < population(parent2_index2,end))
        parent2 = population(parent2_index1, 1:end-1);
    else
        parent2 = population(parent2_index2, 1:end-1);
    end
    
    offspring = union(parent1,parent2);
    offspring = offspring(randperm(length(offspring),n));
end

