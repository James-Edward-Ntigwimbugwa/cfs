package com.example.app.repositories;

import com.example.app.models.User;
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/**
 * User Repository for demoapp
 *
 * This is a simple in-memory repository implementation.
 * Replace this with a proper Spring Data JPA repository when connecting to a database.
 *
 * Example for JPA:
 * public interface UserRepository extends JpaRepository<User, Long> {
 *     Optional<User> findByUsername(String username);
 * }
 */

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    boolean existsByUsername(String username);
    boolean existsByEmail(String email);
}
