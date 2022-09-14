
CREATE TABLE scenario (
	id BIGINT NOT NULL IDENTITY,
	scenario CHAR(3) NOT NULL,
	scenario_name VARCHAR(128) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (scenario)
)



CREATE TABLE unit (
	id BIGINT NOT NULL IDENTITY,
	unit VARCHAR(128) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (unit)
)



CREATE TABLE notation (
	id BIGINT NOT NULL IDENTITY,
	notation VARCHAR(64) NOT NULL,
	notation_name VARCHAR(128) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (notation)
)



CREATE TABLE gas (
	id BIGINT NOT NULL IDENTITY,
	gas VARCHAR(64) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (gas)
)



CREATE TABLE category (
	id BIGINT NOT NULL IDENTITY,
	category VARCHAR(128) NOT NULL,
	category_code VARCHAR(128) NOT NULL,
	category_lulucf VARCHAR(32) NOT NULL,
	category_parent VARCHAR(128) NOT NULL,
	crf_code VARCHAR(128) NOT NULL,
	is_user_defined BIT NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (category)
)



CREATE TABLE country (
	id BIGINT NOT NULL IDENTITY,
	country_code VARCHAR(8) NOT NULL,
	country_name VARCHAR(128) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (country_code)
)



CREATE TABLE parameter (
	id BIGINT NOT NULL IDENTITY,
	parameter VARCHAR(128) NOT NULL,
	default_unit VARCHAR(128) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (parameter),
	FOREIGN KEY(default_unit) REFERENCES unit (unit)
)



CREATE TABLE table_1 (
	id BIGINT NOT NULL,
	country_code VARCHAR(8) NOT NULL,
	category VARCHAR(128) NOT NULL,
	year SMALLINT NOT NULL,
	gas VARCHAR(64) NOT NULL,
	scenario CHAR(3) NOT NULL,
	unit VARCHAR(128) NOT NULL,
	is_ry BIT NOT NULL,
	subtable CHAR(1) NOT NULL,
	notation VARCHAR(64) NOT NULL,
	value FLOAT NOT NULL,
	FOREIGN KEY(country_code) REFERENCES country (country_code),
	FOREIGN KEY(category) REFERENCES category (category),
	FOREIGN KEY(gas) REFERENCES gas (gas),
	FOREIGN KEY(scenario) REFERENCES scenario (scenario),
	FOREIGN KEY(unit) REFERENCES unit (unit),
	FOREIGN KEY(notation) REFERENCES notation (notation)
)



CREATE TABLE table_3 (
	id BIGINT NOT NULL IDENTITY,
	country_code VARCHAR(8) NOT NULL,
	parameter VARCHAR(128) NOT NULL,
	scenario CHAR(3) NOT NULL,
	year SMALLINT NOT NULL,
	default_unit VARCHAR(128) NOT NULL,
	additional_unit VARCHAR(8) NOT NULL,
	notation VARCHAR(64) NOT NULL,
	value FLOAT NOT NULL,
	data_source VARCHAR(1024) NOT NULL,
	comment VARCHAR(512) NOT NULL,
	is_part_of_projections BIT NOT NULL,
	is_ry BIT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(country_code) REFERENCES country (country_code),
	FOREIGN KEY(scenario) REFERENCES scenario (scenario),
	FOREIGN KEY(parameter) REFERENCES parameter (parameter),
	FOREIGN KEY(notation) REFERENCES notation (notation)
)
