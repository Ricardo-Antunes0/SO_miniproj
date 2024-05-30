function population = selection(population,new_population,m)
    elite_individuals = population(1:m,:);
    combined_population = [elite_individuals; new_population];
    population = sortrows(combined_population,size(combined_population,2));
    
    %
    %x = [p1; p2];
    %sortrows(x,size(x,2));
    %p = x(1:m,:);

    % Mas assim nao estamos a obter os 100 individuos, mas sim os 10
    % o objetivo nao e obter 100 individuos da uniao das 2 populacoes
    % e ter no maximo 10 da populacao atual e os restantes da nova?
end