const SchemaService = require('./schemaService');

class CachedSchemaService {
    constructor() {
        this.schemaService = new SchemaService();
        this.cache = null;
        this.lastUpdated = null;
        this.CACHE_DURATION = 1000 * 60 * 60; // 1 hour
    }

    async getSchemas() {
        if (this.shouldRefreshCache()) {
            this.cache = await this.schemaService.getAllSchemas();
            this.lastUpdated = Date.now();
        }
        return this.cache;
    }

    shouldRefreshCache() {
        return !this.cache || 
               !this.lastUpdated || 
               Date.now() - this.lastUpdated > this.CACHE_DURATION;
    }

    getRelevantTables(query) {
        const relevantTables = new Set();
        const keywords = query.toLowerCase().split(' ');
        
        // Add 'transactions' by default as it's our main table
        relevantTables.add('transactions');
        
        // Add tables based on keywords
        if (keywords.some(k => k.includes('user') || k.includes('profile'))) {
            relevantTables.add('users');
        }
        
        return relevantTables;
    }

    filterSchemaForPrompt(schemas, relevantTables) {
        const filtered = {};
        relevantTables.forEach(table => {
            if (schemas[table]) {
                filtered[table] = schemas[table].map(col => ({
                    column: col.column,
                    type: col.type,
                    // Only include essential constraints
                    primaryKey: col.primaryKey,
                    references: col.references
                }));
            }
        });
        return filtered;
    }
}

module.exports = new CachedSchemaService(); 