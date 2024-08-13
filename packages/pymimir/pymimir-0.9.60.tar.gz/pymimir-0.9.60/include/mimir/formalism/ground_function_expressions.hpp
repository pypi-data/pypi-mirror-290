/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef MIMIR_FORMALISM_GROUND_FUNCTION_EXPRESSIONS_HPP_
#define MIMIR_FORMALISM_GROUND_FUNCTION_EXPRESSIONS_HPP_

#include "mimir/formalism/declarations.hpp"

namespace mimir
{

/* FunctionExpressionNumber */
class GroundFunctionExpressionNumberImpl : public loki::Base<GroundFunctionExpressionNumberImpl>
{
private:
    double m_number;

    // Below: add additional members if needed and initialize them in the constructor

    GroundFunctionExpressionNumberImpl(size_t index, double number);

    // Give access to the constructor.
    friend class loki::UniqueValueTypeFactory<GroundFunctionExpressionImpl,
                                              loki::Hash<const GroundFunctionExpressionImpl*, true>,
                                              loki::EqualTo<const GroundFunctionExpressionImpl*, true>>;

    bool is_structurally_equivalent_to_impl(const GroundFunctionExpressionNumberImpl& other) const;
    size_t hash_impl() const;
    void str_impl(std::ostream& out, const loki::FormattingOptions& options) const;

    // Give access to the private interface implementations.
    friend class loki::Base<GroundFunctionExpressionNumberImpl>;

public:
    double get_number() const;
};

/* FunctionExpressionBinaryOperator */
class GroundFunctionExpressionBinaryOperatorImpl : public loki::Base<GroundFunctionExpressionBinaryOperatorImpl>
{
private:
    loki::BinaryOperatorEnum m_binary_operator;
    GroundFunctionExpression m_left_function_expression;
    GroundFunctionExpression m_right_function_expression;

    // Below: add additional members if needed and initialize them in the constructor

    GroundFunctionExpressionBinaryOperatorImpl(size_t index,
                                               loki::BinaryOperatorEnum binary_operator,
                                               GroundFunctionExpression left_function_expression,
                                               GroundFunctionExpression right_function_expression);

    // Give access to the constructor.
    friend class loki::UniqueValueTypeFactory<GroundFunctionExpressionImpl,
                                              loki::Hash<const GroundFunctionExpressionImpl*, true>,
                                              loki::EqualTo<const GroundFunctionExpressionImpl*, true>>;

    bool is_structurally_equivalent_to_impl(const GroundFunctionExpressionBinaryOperatorImpl& other) const;
    size_t hash_impl() const;
    void str_impl(std::ostream& out, const loki::FormattingOptions& options) const;

    // Give access to the private interface implementations.
    friend class loki::Base<GroundFunctionExpressionBinaryOperatorImpl>;

public:
    loki::BinaryOperatorEnum get_binary_operator() const;
    const GroundFunctionExpression& get_left_function_expression() const;
    const GroundFunctionExpression& get_right_function_expression() const;
};

/* FunctionExpressionMultiOperator */
class GroundFunctionExpressionMultiOperatorImpl : public loki::Base<GroundFunctionExpressionMultiOperatorImpl>
{
private:
    loki::MultiOperatorEnum m_multi_operator;
    GroundFunctionExpressionList m_function_expressions;

    // Below: add additional members if needed and initialize them in the constructor

    GroundFunctionExpressionMultiOperatorImpl(size_t index, loki::MultiOperatorEnum multi_operator, GroundFunctionExpressionList function_expressions);

    // Give access to the constructor.
    friend class loki::UniqueValueTypeFactory<GroundFunctionExpressionImpl,
                                              loki::Hash<const GroundFunctionExpressionImpl*, true>,
                                              loki::EqualTo<const GroundFunctionExpressionImpl*, true>>;

    bool is_structurally_equivalent_to_impl(const GroundFunctionExpressionMultiOperatorImpl& other) const;
    size_t hash_impl() const;
    void str_impl(std::ostream& out, const loki::FormattingOptions& options) const;

    // Give access to the private interface implementations.
    friend class loki::Base<GroundFunctionExpressionMultiOperatorImpl>;

public:
    loki::MultiOperatorEnum get_multi_operator() const;
    const GroundFunctionExpressionList& get_function_expressions() const;
};

/* FunctionExpressionMinus */
class GroundFunctionExpressionMinusImpl : public loki::Base<GroundFunctionExpressionMinusImpl>
{
private:
    GroundFunctionExpression m_function_expression;

    // Below: add additional members if needed and initialize them in the constructor

    GroundFunctionExpressionMinusImpl(size_t index, GroundFunctionExpression function_expression);

    // Give access to the constructor.
    friend class loki::UniqueValueTypeFactory<GroundFunctionExpressionImpl,
                                              loki::Hash<const GroundFunctionExpressionImpl*, true>,
                                              loki::EqualTo<const GroundFunctionExpressionImpl*, true>>;

    bool is_structurally_equivalent_to_impl(const GroundFunctionExpressionMinusImpl& other) const;
    size_t hash_impl() const;
    void str_impl(std::ostream& out, const loki::FormattingOptions& options) const;

    // Give access to the private interface implementations.
    friend class loki::Base<GroundFunctionExpressionMinusImpl>;

public:
    const GroundFunctionExpression& get_function_expression() const;
};

/* FunctionExpressionFunction */
class GroundFunctionExpressionFunctionImpl : public loki::Base<GroundFunctionExpressionFunctionImpl>
{
private:
    GroundFunction m_function;

    // Below: add additional members if needed and initialize them in the constructor

    GroundFunctionExpressionFunctionImpl(size_t index, GroundFunction function);

    // Give access to the constructor.
    friend class loki::UniqueValueTypeFactory<GroundFunctionExpressionImpl,
                                              loki::Hash<const GroundFunctionExpressionImpl*, true>,
                                              loki::EqualTo<const GroundFunctionExpressionImpl*, true>>;

    bool is_structurally_equivalent_to_impl(const GroundFunctionExpressionFunctionImpl& other) const;
    size_t hash_impl() const;
    void str_impl(std::ostream& out, const loki::FormattingOptions& options) const;

    // Give access to the private interface implementations.
    friend class loki::Base<GroundFunctionExpressionFunctionImpl>;

public:
    const GroundFunction& get_function() const;
};

}

#endif
