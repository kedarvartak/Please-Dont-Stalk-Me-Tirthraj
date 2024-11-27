const { sequelize } = require('../models');

class SchemaService {
    async getTableSchema(tableName) {
        try {
            const tableInfo = await sequelize.queryInterface.describeTable(tableName);
            
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
            const query = `
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            `;
            const [tables] = await sequelize.query(query);
            
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
}

module.exports = SchemaService; 