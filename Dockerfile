# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Prevent apt from asking questions
ENV DEBIAN_FRONTEND=noninteractive

# Install PostgreSQL and necessary tools
RUN apt-get update && \
    apt-get install -y net-tools postgresql postgresql-contrib sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Adjust PostgreSQL configurations for remote and local connections
RUN sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/14/main/postgresql.conf && \
    sed -i "s/local   all             all                                     peer/local   all             all                                     trust/g" /etc/postgresql/14/main/pg_hba.conf && \
    sed -i "s/local   all             postgres                                peer/local   all             postgres                                trust/g" /etc/postgresql/14/main/pg_hba.conf && \
    echo "host all  all    0.0.0.0/0    md5" >> /etc/postgresql/14/main/pg_hba.conf && \
    echo "host all  all    127.0.0.1/32  md5" >> /etc/postgresql/14/main/pg_hba.conf

# Copy the database dump tar file into the container
COPY phase4.tar /tmp/phase4.tar

# Create a directory to unpack the tar file, extract it, and adjust permissions
RUN mkdir /tmp/phase4 && \
    tar -xvf /tmp/phase4.tar -C /tmp/phase4 && \
    chmod -R 755 /tmp/phase4  # Adjusting permissions

# Copy the database dump SQL file into the container
COPY restore.sql /tmp/phase4/restore.sql

# Start PostgreSQL, set the password for the postgres user, and perform database operations
RUN service postgresql start && \
    sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'student';" && \
    sed -i "s/local   all             postgres                                trust/local   all             postgres                                md5/g" /etc/postgresql/14/main/pg_hba.conf && \
    sed -i "s/local   all             all                                     trust/local   all             all                                     md5/g" /etc/postgresql/14/main/pg_hba.conf && \
    sudo -u postgres createdb phase4 && \
    sudo -u postgres psql -d phase4 -f /tmp/phase4/restore.sql && \
    service postgresql stop

EXPOSE 5432

# Use the postgres command to start PostgreSQL as the last step.
CMD ["sudo", "-u", "postgres", "/usr/lib/postgresql/14/bin/postgres", "-D", "/var/lib/postgresql/14/main", "-c", "config_file=/etc/postgresql/14/main/postgresql.conf"]

