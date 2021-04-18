'use strict';

const express = require('express');
const mysql = require('promise-mysql');
const bodyParser = require('body-parser');

const app = express();
app.set('view engine', 'pug');
app.enable('trust proxy');

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

app.use((req, res, next) => {
  res.set('Content-Type', 'text/html');
  next();
});

const winston = require('winston');
const {LoggingWinston} = require('@google-cloud/logging-winston');
const loggingWinston = new LoggingWinston();
const logger = winston.createLogger({
  level: 'info',
  transports: [new winston.transports.Console(), loggingWinston],
});

// [START cloud_sql_mysql_mysql_create_tcp]
const createTcpPool = async config => {
  // Extract host and port from socket address
  const dbSocketAddr = process.env.DB_HOST.split(':');

  // Establish a connection to the database
  return await mysql.createPool({
    user: poccomposer, // e.g. 'my-db-user'
    password: poccomposer, // e.g. 'my-db-password'
    database: calendar, // e.g. 'my-database'
    host: dbSocketAddr[0], // e.g. '127.0.0.1'
    port: dbSocketAddr[1], // e.g. '3306'
    // ... Specify additional properties here.
    ...config,
  });
};
// [END cloud_sql_mysql_mysql_create_tcp]

// [START cloud_sql_mysql_mysql_create_socket]
const createUnixSocketPool = async config => {
  const dbSocketPath = process.env.DB_SOCKET_PATH || '/cloudsql';

  // Establish a connection to the database
  return await mysql.createPool({
    user: poccomposer, // e.g. 'my-db-user'
    password: poccomposer, // e.g. 'my-db-password'
    database: calendar, // e.g. 'my-database'
    // If connecting via unix domain socket, specify the path
    socketPath: `${dbSocketPath}/solid-silicon-310213:southamerica-east1:poccomposer`,
    // Specify additional properties here.
    ...config,
  });
};
// [END cloud_sql_mysql_mysql_create_socket]

const createPool = async () => {
  const config = {
    connectionLimit: 5,
    connectTimeout: 10000, // 10 seconds
    acquireTimeout: 10000, // 10 seconds
    waitForConnections: true, // Default: true
    queueLimit: 0, // Default: 0
  };
  if (process.env.DB_HOST) {
    return await createTcpPool(config);
  } else {
    return await createUnixSocketPool(config);
  }
};

const ensureSchema = async pool => {
  await pool.query(
    `CREATE TABLE IF NOT EXISTS holidays ( 
        date NULL,
        PRIMARY KEY (date) 
      );`
  );
};

const createPoolAndEnsureSchema = async () =>
  await createPool()
    .then(async pool => {
      await ensureSchema(pool);
      return pool;
    })
    .catch(err => {
      logger.error(err);
      throw err;
    });

let pool;

app.use(async (req, res, next) => {
  if (pool) {
    return next();
  }
  try {
    pool = await createPoolAndEnsureSchema();
    next();
  } catch (err) {
    logger.error(err);
    return next(err);
  }
});

// Serve the index page, showing vote tallies.
app.get('/', async (req, res) => {
  pool = pool || (await createPoolAndEnsureSchema());
  try {
    const stmt = 'select count(*) from holidays where date=DATE(now())';
    // This is faster than await-ing each query object as it is created
    return await stmt;

} catch (err) {
    logger.error(err);
    res
      .status(500)
      .send(
        'Unable to load page. Please check the application logs for more details.'
      )
      .end();
  }
});

const PORT = process.env.PORT || 8080;
const server = app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

process.on('unhandledRejection', err => {
  console.error(err);
  throw err;
});

module.exports = server;