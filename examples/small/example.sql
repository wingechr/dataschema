
CREATE TABLE country (
	id BIGINT NOT NULL IDENTITY,
	country_code VARCHAR(8) NOT NULL,
	country_name VARCHAR(128) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (country_code)
)



CREATE TABLE table_1 (
	id BIGINT NOT NULL IDENTITY,
	country_code VARCHAR(8) NOT NULL,
	year SMALLINT NOT NULL,
	value FLOAT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(country_code) REFERENCES country (country_code)
)
