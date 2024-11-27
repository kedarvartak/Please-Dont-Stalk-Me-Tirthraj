const { sequelize } = require('../models');

class SchemaService {
    async getTableSchema(tableName) {
        try {
            // Get table information using Sequelize's queryInterface
            const tableInfo = await sequelize.queryInterface.describeTable(tableName);
            
            // Format the schema information
            const formattedSchema = Object.entries(tableInfo).map(([columnName, details]) => ({
                column: columnName,
                type: details.type,
                allowNull: details.allowNull,
                defaultValue: details.defaultValue,
                primaryKey: details.primaryKey,
                references: details.references
            }));

            return formattedSchema;
        } catch (error) {
            console.error(`Error fetching schema for table ${tableName}:`, error);
            throw new Error('Failed to fetch database schema');
        }
    }

    async getAllSchemas() {
        try {
            // Get all table names from the database
            const query = `
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            `;
            const [tables] = await sequelize.query(query);
            
            // Get schema for each table
            const schemas = {};
            for (const { table_name } of tables) {
                schemas[table_name] = await this.getTableSchema(table_name);
            }
            
            return schemas;
        } catch (error) {
            console.error('Error fetching all schemas:', error);
            throw new Error('Failed to fetch database schemas');
        }
    }

    formatSchemaForPrompt(schemas) {
        let prompt = 'Database Schema:\n';
        
        Object.entries(schemas).forEach(([tableName, columns]) => {
            prompt += `\nTable: ${tableName}\nColumns:\n`;
            columns.forEach(column => {
                prompt += `- ${column.column} (${column.type})`;
                if (column.primaryKey) prompt += ' PRIMARY KEY';
                if (column.references) prompt += ` REFERENCES ${column.references.table}(${column.references.key})`;
                if (!column.allowNull) prompt += ' NOT NULL';
                prompt += '\n';
            });
        });
        
        return prompt;
    }
}

module.exports = new SchemaService(); 