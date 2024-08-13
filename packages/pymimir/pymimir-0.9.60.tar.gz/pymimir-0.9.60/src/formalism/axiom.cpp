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

#include "mimir/formalism/axiom.hpp"

#include "mimir/common/collections.hpp"
#include "mimir/common/concepts.hpp"
#include "mimir/common/hash.hpp"
#include "mimir/common/printers.hpp"
#include "mimir/formalism/literal.hpp"
#include "mimir/formalism/variable.hpp"

#include <cassert>

namespace mimir
{
AxiomImpl::AxiomImpl(size_t index,
                     VariableList parameters,
                     Literal<Derived> literal,
                     LiteralList<Static> static_conditions,
                     LiteralList<Fluent> fluent_conditions,
                     LiteralList<Derived> derived_conditions) :
    Base(index),
    m_parameters(std::move(parameters)),
    m_literal(std::move(literal)),
    m_static_conditions(std::move(static_conditions)),
    m_fluent_conditions(std::move(fluent_conditions)),
    m_derived_conditions(std::move(derived_conditions))
{
    assert(!literal->is_negated());
    assert(is_all_unique(m_parameters));
    assert(is_all_unique(m_static_conditions));
    assert(is_all_unique(m_fluent_conditions));
    assert(is_all_unique(m_derived_conditions));

    /* Canonize. */
    std::sort(m_static_conditions.begin(), m_static_conditions.end(), [](const auto& l, const auto& r) { return l->get_index() < r->get_index(); });
    std::sort(m_fluent_conditions.begin(), m_fluent_conditions.end(), [](const auto& l, const auto& r) { return l->get_index() < r->get_index(); });
    std::sort(m_derived_conditions.begin(), m_derived_conditions.end(), [](const auto& l, const auto& r) { return l->get_index() < r->get_index(); });
}

bool AxiomImpl::is_structurally_equivalent_to_impl(const AxiomImpl& other) const
{
    if (this != &other)
    {
        return (m_literal == other.m_literal) && (m_static_conditions == other.m_static_conditions) && (m_fluent_conditions == other.m_fluent_conditions)
               && (m_derived_conditions == other.m_derived_conditions);
    }
    return true;
}

size_t AxiomImpl::hash_impl() const { return HashCombiner()(m_literal, m_static_conditions, m_fluent_conditions, m_derived_conditions); }

void AxiomImpl::str_impl(std::ostream& out, const loki::FormattingOptions& options) const
{
    auto nested_options = loki::FormattingOptions { options.indent + options.add_indent, options.add_indent };
    out << std::string(options.indent, ' ') << "(:derived " << *m_literal << std::endl;
    out << std::string(nested_options.indent, ' ') << "(and";
    for (const auto& condition : m_static_conditions)
    {
        out << " " << *condition;
    }
    for (const auto& condition : m_fluent_conditions)
    {
        out << " " << *condition;
    }
    for (const auto& condition : m_derived_conditions)
    {
        out << " " << *condition;
    }
    out << ")" << std::endl;
    out << std::string(options.indent, ' ') << ")" << std::endl;
}

const VariableList& AxiomImpl::get_parameters() const { return m_parameters; }

const Literal<Derived>& AxiomImpl::get_literal() const { return m_literal; }

template<PredicateCategory P>
const LiteralList<P>& AxiomImpl::get_conditions() const
{
    if constexpr (std::is_same_v<P, Static>)
    {
        return m_static_conditions;
    }
    else if constexpr (std::is_same_v<P, Fluent>)
    {
        return m_fluent_conditions;
    }
    else if constexpr (std::is_same_v<P, Derived>)
    {
        return m_derived_conditions;
    }
    else
    {
        static_assert(dependent_false<P>::value, "Missing implementation for PredicateCategory.");
    }
}

template const LiteralList<Static>& AxiomImpl::get_conditions<Static>() const;
template const LiteralList<Fluent>& AxiomImpl::get_conditions<Fluent>() const;
template const LiteralList<Derived>& AxiomImpl::get_conditions<Derived>() const;

size_t AxiomImpl::get_arity() const { return m_parameters.size(); }

}
