const { GoogleGenerativeAI } = require('@google/generative-ai');
const schemaService = require('./schemaService');

class NLPService {
    constructor() {
        if (!process.env.GEMINI_API_KEY) {
            throw new Error('GEMINI_API_KEY is required');
        }
        console.log('API Key length:', process.env.GEMINI_API_KEY.length);
        const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
        this.model = genAI.getGenerativeModel({ model: "gemini-pro" });
    }

    async processQuery(query, userId) {
        const schemas = await schemaService.getAllSchemas();
        const schemaPrompt = this.formatSchemaForPrompt(schemas);

        const prompt = `You are a financial analyst AI that converts natural language queries into PostgreSQL queries.
            
            ${schemaPrompt}

            User Question: ${query}

            Requirements:
            1. Always include "userId" = $1 in WHERE clause
            2. Return only relevant financial data
            3. Never include the actual userId value in the SQL
            4. Always use $1 for the userId parameter
            5. Always use double quotes around column names
            6. Use lowercase for type values ('expense', 'income')
            7. For date functions, use CURRENT_DATE - INTERVAL '1 month'

            Response Format:
            1. Start your response with \`\`\`sql
            2. Write the SQL query
            3. End with \`\`\`
            4. No additional text or explanations

            Example Response:
            \`\`\`sql
            SELECT "amount", "category", "type" 
            FROM "transactions" 
            WHERE "userId" = $1 
            ORDER BY "amount" DESC
            \`\`\`

            Now generate the SQL query for the user question:`;

        try {
            const result = await this.model.generateContent(prompt);
            let sql = result.response.text().trim();
            
            // Remove any code block markers or SQL prefixes
            sql = sql.replace(/```(?:sql)?/g, '').trim();
            
            // Basic validation
            if (!sql.toUpperCase().includes('SELECT')) {
                throw new Error('Response must be a SELECT query');
            }
            
            if (!sql.includes('"userId"') || !sql.includes('$1')) {
                throw new Error('Query must include userId parameter');
            }

            return {
                sql,
                explanation: this.generateExplanation(sql)
            };

        } catch (error) {
            console.error('NLP Service Error:', error);
            throw new Error(`Failed to process query: ${error.message}`);
        }
    }

    formatSchemaForPrompt(schemas) {
        return Object.entries(schemas)
            .map(([tableName, columns]) => {
                const columnDefs = columns
                    .map(col => `    - ${col.column} (${col.type})`)
                    .join('\n');
                return `Table: ${tableName}\nColumns:\n${columnDefs}`;
            })
            .join('\n\n');
    }

    generateExplanation(sql) {
        const hasGroupBy = sql.toLowerCase().includes('group by');
        const hasOrderBy = sql.toLowerCase().includes('order by');
        const hasAggregate = /sum|avg|count|min|max/i.test(sql);
        
        let explanation = "This query retrieves";
        if (hasAggregate) explanation += " aggregated";
        explanation += " financial data";
        if (hasGroupBy) explanation += " grouped by specific categories";
        if (hasOrderBy) explanation += " in a sorted order";
        
        return explanation + " for your transactions.";
    }
}

module.exports = new NLPService();