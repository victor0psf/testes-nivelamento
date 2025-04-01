SELECT 
    o.registro_ans,
    o.nome_fantasia,
    SUM(d.valor) AS total_despesas,
    o.uf
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.registro_ans = o.registro_ans
WHERE 
    d.descricao LIKE '%EVENTOS/%SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.tipo = 'despesa'
    AND d.competencia >= DATE_SUB(
        (SELECT MAX(competencia) FROM demonstracoes_contabeis), 
        INTERVAL 3 MONTH
    )
GROUP BY 
    o.registro_ans, o.nome_fantasia, o.uf
ORDER BY 
    total_despesas DESC
LIMIT 10;