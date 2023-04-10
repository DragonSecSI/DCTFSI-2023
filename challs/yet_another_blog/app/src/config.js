const fs = require("fs");
const path = require("path");
const joi = require("joi");
const crypto = require("crypto");
const isDev = process.env.NODE_ENV !== "production";
if (isDev) {
  require("dotenv").config({
    path: path.join(__dirname, "../../.env"),
  });
}

// Validate environment variables
const envVarsSchema = joi
  .object({
    NODE_ENV: joi.string().allow("development", "production").required(),
    FLAG: joi.string().required(),
    HOST: joi.string().optional().default("0.0.0.0"),
    PORT: joi.number().positive().optional().default(3000),
    FQDN: joi.string(),
  })
  .unknown();

const { error, value: envVars } = envVarsSchema.validate(process.env);

if (error) {
  throw new Error(`Config validation error: ${error.message}`);
}
const { FLAG, HOST, PORT, FQDN } = envVars;

// Read keys from key directory
const SECRETS_DIR = `/etc/letsencrypt/live/${FQDN}`;
const PRIV_KEY = fs.readFileSync(`${SECRETS_DIR}/privkey.pem`);
const PUB_KEY = fs.readFileSync(`${SECRETS_DIR}/cert.pem`);

// Random password for admin login
const ADMIN_PASSWORD = isDev ? "admin" : crypto.randomBytes(16).toString("hex");

console.log(`This session's admin password is: ${ADMIN_PASSWORD}`);
module.exports = { PRIV_KEY, PUB_KEY, ADMIN_PASSWORD, PORT, FLAG, HOST };
