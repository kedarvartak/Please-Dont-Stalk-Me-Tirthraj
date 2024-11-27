const nlpService = require('../services/nlpService');
const { sequelize } = require('../models');

exports.processQuery = async (req, res) => {
    try {
        const { query } = req.body;
        console.log('Received query:', query);

        if (!query) {
            return res.status(400).json({ 
                error: 'Missing query parameter',
                details: 'Query cannot be empty'
            });
        }

        const user = await sequelize.models.User.findOne();
        if (!user) {
            return res.status(404).json({ 
                error: 'No test user found',
                details: 'Please ensure test data is loaded'
            });
        }

        console.log('Processing query with NLP service');
        const response = await nlpService.processQuery(query, user.id);
        
        // Extract SQL from response
        const sqlQuery = typeof response === 'string' ? response : response.sql;
        console.log('Generated SQL:', sqlQuery);

        console.log('Executing SQL query with params:', [user.id]);
        const results = await sequelize.query(
            sqlQuery,
            {
                bind: [user.id],
                type: sequelize.QueryTypes.SELECT
            }
        );
        console.log('Query results:', results);

        res.json({
            results,
            explanation: response.explanation || "Query executed successfully",
            sql: sqlQuery
        });
    } catch (error) {
        console.error('Controller error:', error);
        res.status(500).json({ 
            error: 'Error processing query',
            details: error.message
        });
    }
}; 