# README

## Example

`sharedColumns.json`: shared column definitions as json schema

```json
{
  "id": {
    "name": "id",
    "description": "unique id",
    "type": "bigint"
  },
  "year": {
    "name": "year",
    "description": "year for which projected data is reported",
    "type": "smallint"
  },
  "country_code": {
    "name": "country_code",
    "description": "Code used to abbreviate country name",
    "type": "varchar(8)"
  },
  "value": {
    "name": "value",
    "description": "value reported",
    "type": "float"
  }
}
```

`example.json`: table definitions as json schema

```json
{
  "columns": {
    "$ref": "sharedColumns.json"
  },
  "resources": [
    {
      "name": "country",
      "schema": {
        "primaryKey": "id",
        "uniqueKeys": ["country_code"],
        "fields": [
          {
            "$ref": "#/columns/id"
          },
          {
            "$ref": "#/columns/country_code"
          },
          {
            "name": "country_name",
            "description": "Full country name in english",
            "type": "varchar(128)"
          }
        ]
      }
    },
    {
      "name": "table_1",
      "schema": {
        "primaryKey": "id",
        "foreignKeys": [
          {
            "fields": "country_code",
            "reference": {
              "resource": "country"
            }
          }
        ],
        "fields": [
          {
            "$ref": "#/columns/id"
          },
          {
            "$ref": "#/columns/country_code"
          },
          {
            "$ref": "#/columns/year"
          },
          {
            "$ref": "#/columns/value"
          }
        ]
      }
    }
  ]
}
```

```bash
python dataschema.py --sql-dialect mssql example.json example.sql
python dataschema.py example.json example.png
```

creates a class diagram (`example.png`)

![example class diagram](examples/small/example.png)

as well as the DDL statements (`example.sql`)

```sql
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
```
