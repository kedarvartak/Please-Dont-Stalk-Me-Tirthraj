const { sequelize, User, Transaction } = require('../models');

async function initializeDatabase() {
    try {
        // Sync all models with database
        await sequelize.sync({ force: true });
        console.log('Database synchronized successfully');

        // Create test user first and wait for it to complete
        const user = await User.create({
            email: 'test@example.com',
            password: 'password123'
        });
        console.log('Test user created with ID:', user.id);

        // Now create transactions using the actual user ID
        const transactions = await Transaction.bulkCreate([
            {
                userId: user.id,  // Use the actual user ID
                type: 'expense',
                amount: 50.00,
                category: 'groceries',
                description: 'Weekly groceries'
            },
            {
                userId: user.id,  // Use the actual user ID
                type: 'income',
                amount: 2000.00,
                category: 'salary',
                description: 'Monthly salary'
            }
        ]);

        console.log(`Created ${transactions.length} test transactions`);
        console.log('Database initialization completed successfully');
        process.exit(0);
    } catch (error) {
        console.error('Error initializing database:', error);
        process.exit(1);
    }
}

initializeDatabase(); 