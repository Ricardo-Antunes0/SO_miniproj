function s_mutated = mutation(s, G)
    others= setdiff(1:numnodes(G),s);
    gene = others(randi(length(others)));
    index_replace = randi(length(s));
    s_mutated = s;
    s_mutated(index_replace) = gene;
end