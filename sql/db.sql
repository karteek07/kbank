CREATE TABLE bank (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    balance TEXT,
    lasttrandt DATETIME
);
CREATE TABLE banker (
    bid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    bpass TEXT NOT NULL,
    btype TEXT NOT NULL,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL
);
CREATE TABLE customer (
    cid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ctype TEXT DEFAULT '01',
    title TEXT NOT NULL,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    dob TEXT NOT NULL,
    gender TEXT NOT NULL,
    maritalstatus TEXT NOT NULL,
    annualincome TEXT NOT NULL,
    fathername TEXT NOT NULL,
    mothername TEXT NOT NULL,
    add1 TEXT NOT NULL,
    add2 TEXT NOT NULL,
    add3 TEXT,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    city TEXT NOT NULL,
    pincode TEXT NOT NULL,
    aadharno TEXT UNIQUE NOT NULL,
    panno TEXT UNIQUE NOT NULL,
    primaryno TEXT NOT NULL,
    secondaryno TEXT,
    email TEXT NOT NULL,
    createdt DATETIME DEFAULT (datetime('now', 'localtime')),
    modifydt DATETIME
);
CREATE TABLE account (
    aid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    cid INTEGER NOT NULL,
    atype TEXT NOT NULL,
    interestrate TEXT NOT NULL,
    purpose TEXT NOT NULL,
    balance TEXT,
    amount TEXT,
    term TEXT,
    finalamount TEXT,
    interestamount TEXT,
    monthlyinstallment TEXT,
    lasttrandt DATETIME,
    createdt DATETIME DEFAULT (datetime('now', 'localtime')),
    name1 TEXT NOT NULL,
    name2 TEXT NOT NULL,
    relation1 TEXT NOT NULL,
    relation2 TEXT NOT NULL,
    add1 TEXT NOT NULL,
    add2 TEXT NOT NULL,
    aadharno1 TEXT NOT NULL,
    aadharno2 TEXT NOT NULL,
    contactno1 TEXT NOT NULL,
    contactno2 TEXT NOT NULL
);
CREATE TABLE transactions (
    tid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    aid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    atype TEXT NOT NULL,
    ttype TEXT NOT NULL,
    aid2 TEXT DEFAULT '' ,
    amount TEXT NOT NULL,
    description TEXT NOT NULL,
    dt DATETIME DEFAULT (datetime('now', 'localtime'))
);
INSERT INTO bank VALUES (101, 'K-Bank', 'Ulhasnagar', '10000000', 0);
INSERT INTO banker (bid, bpass, btype, fname, lname) VALUES (101, 'pass@123', '01', 'Kartik', 'Kamble');
INSERT INTO customer (cid, title, fname, lname, dob, gender, maritalstatus, annualincome, fathername, mothername, add1, add2, add3, state, district, city, pincode, aadharno, panno, primaryno, secondaryno, email)
VALUES (100001, '01', 'Kartik', 'Kamble', '1999-01-07', '01', '01', '01', 'Raja', 'Sunita', 'Near ATP Hindi School', 'Punjabi Colony', 'Ulhasnagar-3', '15', 'Thane', 'Ulhasnagar', '421003', '0000 0000 0001', '0000000001', '9765398789', '0000000000', 'kartik71900@gmail.com');
INSERT INTO account (aid, cid, atype, interestrate, purpose, balance, name1, name2, relation1, relation2, add1, add2, aadharno1, aadharno2, contactno1, contactno2)
VALUES (200001, 100001, '01', '01', 'Savings', '1000', 'Raja', 'Sunita', '01', '02', 'Near ATP Hindi School, Punjabi Colony', 'Near ATP Hindi School, Punjabi Colony', '0000 0000 0000', '1111 1111 1111', '0000000000', '1111111111');
INSERT INTO transactions VALUES (1, 200001, 100001, '01', '01', '1000', 'Initial Deposit', datetime('now', 'localtime'));
UPDATE bank
SET balance = CAST((CAST(balance AS INTEGER) + 1000) AS TEXT)
WHERE id=101;

CREATE TRIGGER account_lasttrandt_trigger
BEFORE UPDATE ON account 
FOR EACH ROW 
BEGIN
UPDATE account
SET lasttrandt = datetime('now', 'localtime')
WHERE aid = OLD.aid;
END;

CREATE TRIGGER bank_lasttrandt_trigger
BEFORE UPDATE ON bank
FOR EACH ROW 
BEGIN
UPDATE bank
SET lasttrandt = datetime('now', 'localtime')
WHERE id = OLD.id;
END;