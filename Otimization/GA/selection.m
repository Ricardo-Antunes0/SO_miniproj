function population = selection(population,new_population,m)
    combined_population = [population(1:m,:), new_population(1:end,:)];
    sortrows(combined_population, size(combined_population,2));
    population = combined_population(1:end-m,:);
end